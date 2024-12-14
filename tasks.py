import os
import shutil
import sys

from invoke import task, Context, Collection
import subprocess

ALLOWED_VERSION_TYPES = ["release", "bug", "feature"]

DOCKER_NAME = "allure-report"  # default name for Docker image
DOCKER_FOLDERS = {  # <image name>: <build context folder>
    "backend": "docker/backend",
    "celeryworker": "docker/celeryworker",
    "nginx": "docker/nginx",
    "postgres": "docker/postgres",
    "redis": "docker/redis",
    "tests": "docker/tests",
}
BUILD_TASK_PREFIX = 'build'


@task
def version(c: Context):
    """Show the current version."""
    with open("src/__about__.py", "r") as f:
        version_line = f.readline()
        version_num = version_line.split('"')[1]
        print(version_num)
        return version_num


def ver_task_factory(version_type: str):
    @task
    def ver(c: Context):
        """Bump the version."""
        c.run(f"./scripts/verup_action.sh {version_type}")

    return ver


@task
def compile_requirements(c: Context):
    """Convert requirements.in to requirements.txt and requirements.dev.txt."""
    start_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    c.run("uv pip compile requirements/requirements.celery.in --output-file=docker/celeryworker/requirements.txt --upgrade")
    c.run("uv pip compile requirements/requirements.in --output-file=docker/backend/requirements.txt --upgrade")
    reqs_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    c.run("uv pip compile requirements/requirements.dev.in --output-file=docker/tests/requirements.txt --upgrade")
    end_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    print(f"Req's compilation time: {int(reqs_time) - int(start_time)} seconds")
    print(f"Req's dev compilation time: {int(end_time) - int(reqs_time)} seconds")
    print(f"Total execution time: {int(end_time) - int(start_time)} seconds")


@task(pre=[compile_requirements])
def reqs(c: Context):
    """Upgrade requirements including pre-commit."""
    c.run("pre-commit autoupdate")
    c.run("uv pip install -r docker/tests/requirements.txt")


@task
def uv(c: Context):
    """Install or upgrade uv."""
    c.run("curl -LsSf https://astral.sh/uv/install.sh | sh")


@task
def pre(c):
    """Run pre-commit checks"""
    c.run("pre-commit run --verbose --all-files")


@task
def run(c):
    """Run the action locally."""
    c.run("docker-compose -f tests/resources/docker-compose.yml up  --build")


@task
def logs(c):
    """Show the logs of the action."""
    c.run("docker-compose -f tests/resources/docker-compose.yml logs")

@task
def rm(c):
    """Show the logs of the action."""
    c.run("docker-compose -f tests/resources/docker-compose.yml rm -f")

@task
def container(c):
    """Enter the container."""
    c.run(
        "docker-compose -f tests/resources/docker-compose.yml run -it --entrypoint="
        " --build upn"
    )


def docker_build_task_factory(name, target_dir):
    @task
    def docker_build(c):
        """Build Docker image. Place local-specific setup scripts to ../../docker-scripts."""
        shared_scripts_dir = "../../docker-scripts"
        scripts_copy_dir = '.setup-scripts'
        try:
            args = ""  # "--no-cache"
            if os.path.exists(shared_scripts_dir):
                os.makedirs(scripts_copy_dir, exist_ok=True)
                shutil.copytree(shared_scripts_dir, scripts_copy_dir, dirs_exist_ok=True)
                args += f" --build-arg SSL_CERT_FILE=/usr/local/share/ca-certificates/custom_cacert.crt"
            args += f" -t {DOCKER_NAME if name == BUILD_TASK_PREFIX else name.split('-')[-1]}"
            c.run(f"docker build {args} -f {target_dir}/Dockerfile .")
        finally:
            if os.path.exists(scripts_copy_dir):
                shutil.rmtree(scripts_copy_dir)
                pass

    return docker_build


namespace = Collection.from_module(sys.modules[__name__])
for name in ALLOWED_VERSION_TYPES:
    namespace.add_task(ver_task_factory(name), name=f"ver-{name}")
for name, folder in DOCKER_FOLDERS.items():
    task_name = f"{BUILD_TASK_PREFIX}-{name}" if name else BUILD_TASK_PREFIX
    namespace.add_task(docker_build_task_factory(task_name, folder), name=task_name)
