import os
import pipes
import subprocess
import logging

logger = logging.getLogger(__name__)


def run(command):

    logger.debug(command)

    # logger.info(os.environ['PATH'])

    process = subprocess.Popen(
        [command],
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout = process.stdout.readline()
    stderr = process.stderr.readline()

    if stdout:
        logger.info(stdout)
    if stderr:
        logger.warning(stderr)


def preBuild(site):

    scss_import_path = os.path.join(site.static_path, "lib", "bourbon")


    run('find %s -name "*.sass" -not -name "_*" -exec sass -C --update --load-path %s {} \;' %
        (pipes.quote(site.static_path), pipes.quote(scss_import_path)))

    run('find %s -name "*.coffee" -exec coffee -c {} \;' % pipes.quote(site.static_path))


def preDeploy(site):

    logger.info('Predeploying!')
    run('pwd')

    # TODO minify js, minify css, hash version files
