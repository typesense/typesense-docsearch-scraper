from .abstract_command import AbstractCommand


class AbstractBuildDocker(AbstractCommand):
    @staticmethod
    def build_docker_file(file, image="typesense/docsearch-scraper-dev",
                          local_tag=False):
        tags = [image]
        AbstractBuildDocker.setup_buildx()

        if local_tag:
            tag = AbstractBuildDocker.get_local_tag().decode()
            tags.append(image + ":" + tag)

        cmd = ["docker", "buildx", "build"] + [param for tag in tags for param in
                                     ['-t', tag]] + ["-f", file, "."]
        if local_tag:
            cmd += ["--platform", "linux/amd64,linux/arm64", "--push"]
        else:
            cmd += ["--load"]

        return AbstractCommand.exec_shell_command(cmd)

    def get_options(self):
        return [{"name": "local_tag",
                 "description": "tag image according to source git tag",
                 "optional": False}]

    @staticmethod
    def get_local_tag():
        from subprocess import check_output
        return check_output(
            ['git', 'describe', '--abbrev=0', '--tags']).strip()

    @staticmethod
    def setup_buildx():
        from subprocess import check_output, CalledProcessError
        try:
            return check_output(['docker', 'buildx', 'use', 'typesense-builder']).strip()
        except CalledProcessError:
            return check_output(['docker', 'buildx', 'create', '--name', 'typesense-builder', '--driver', 'docker-container', '--use', '--bootstrap']).strip()
