import itertools

__version__ = '0.2.10'

def xrepr(arg):
    if isinstance(arg, str):
        return "'%s'" % arg
    else:
        return repr(arg)


def get_generated_warning():
    return """\
#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################
"""


def get_params(php, os, variant):
    """Configuration parameters for php with their default values"""

    params = dict()
    if variant == 'cli':
        params.update({
            'PHP_UID': 1000,
            'PHP_GID': 1000
        })

    return params


def get_env_defaults_str(php, os, variant):
    items = get_params(php, os, variant).items()
    return '\n'.join(("DEFAULT_%s=%s" % (k, xrepr(v)) for k, v in items))


def get_env_settings_str(php, os, variant):
    params = list(get_params(php, os, variant))
    return '\n'.join(('%s=${%s-$DEFAULT_%s}' % (k, k, k) for k in params))


def get_docker_args_str(php, os, variant):
    items = get_params(php, os, variant).items()
    if len(items) == 0: return ''
    return '\n'.join(('ARG %s=%s' % (k, xrepr(v)) for k, v in items))


def get_docker_env_str(php, os, variant):
    params = list(get_params(php, os, variant))
    if len(params) == 0: return ''
    return 'ENV ' + ' \\\n    '.join(('%s=$%s' % (k, k) for k in params))


def get_context_dir(php, os, variant, sep='/'):
    return sep.join([x for x in [php, os, variant] if x is not None])


def get_tag(php=None, os=None, variant=None, sep='-'):
    return sep.join([x for x in [php, variant, os] if x is not None])


def get_tag_aliases(php, os, variant):
    aliases = []
    vgroup = [t for t in get_matrix() if php == t[0] and variant == t[2]]
    maj = get_tag(php.split('.')[0])

    if 'cli' == variant:
        aliases.append(get_tag(php, os, None))

    if vgroup[-1][1] == os: # latest os in a grup
        aliases.append(get_tag(php, None, variant))
        if 'cli' == variant:
            aliases.append(get_tag(php, None, None))

    if phps()[-1] == php and oses()[-1] == os:
        aliases.append(get_tag(maj, None, variant))
        if 'cli' == variant:
            aliases.append(get_tag(maj))
        aliases.append(get_tag('latest', None, variant))
        aliases.append(get_tag(None, None, variant))
        if 'cli' == variant:
            aliases.append(get_tag('latest'))
    return aliases


def get_tags(php, os, variant):
    return [get_tag(php, os, variant)] + get_tag_aliases(php, os, variant)


def get_context_files(php, os, variant):
    return {'Dockerfile.%s' % variant: 'Dockerfile',
            'hooks/build.in': 'hooks/build' }


def get_microbadges_str_for_tag(tag):
    name = 'korowai/php:%(tag)s' % locals()
    url1 = 'https://images.microbadger.com/badges'
    url2 = 'https://microbadger.com/images/%(name)s' % locals()
    return "\n".join([
        '[![](%(url1)s/version/%(name)s.svg)](%(url2)s "%(name)s")' % locals(),
        '[![](%(url1)s/image/%(name)s.svg)](%(url2)s "Docker image size")' % locals(),
        '[![](%(url1)s/commit/%(name)s.svg)](%(url2)s "Source code")' % locals()
  ])


def get_microbadges_str_for_tags(tags):
    return '- ' + "\n- ".join(reversed([get_microbadges_str_for_tag(tag) for tag in tags]))


def get_microbadges_str(matrix):
    #seen = set([])
    lines = []
    for (php, os, variant) in reversed(matrix):
        lines.append("")
        lines.append("### %s" % get_tag(php, os, variant))
        lines.append("")
        tag = get_tag(php, os, variant)
        lines.append(get_microbadges_str_for_tag(tag))
        aliases = get_tag_aliases(php, os, variant)
        if aliases:
            lines.append("")
            lines.append("aliases: %s" % ', '.join(aliases))
            lines.append("")
        #tags = get_tags(php, os, variant)
        #lines.append(get_microbadges_str_for_tags(tags))
    return "\n".join(lines)


def get_circle_job_name(php, os, variant):
    return "build_%s_%s_%s" % (php.replace('.','_'), variant, os)


def get_circle_jobs_str(matrix):
    jobs = []
    for m in matrix:
        php, os, variant = m
        s = "\n  ".join([
            "%s:" % get_circle_job_name(php, os, variant),
            "  <<: *executor",
            "  environment:",
            "    <<: *env_common",
            "    DOCKERFILE_PATH: %s" % get_context_dir(php, os, variant),
            "    IMAGE_NAME: korowai/php:%s" % get_tag(php, os, variant),
            "    DOCKER_TAG: %s" % (','.join(get_tags(php, os, variant))),
            "  <<: *build_steps"
            ])
        jobs.append(s)
    return "\n\n  ".join(jobs)


def get_circle_workflow_jobs_str(matrix):
    lines = []
    for (php, os, variant) in matrix:
        lines.append("- %s:" % get_circle_job_name(php, os, variant))
        lines.append("    context: korowai-docker")
    return "\n      ".join(lines)


def get_common_subst():
    return dict({ 'GENERATED_WARNING' : get_generated_warning(),
                  'VERSION': __version__ })


def get_context_subst(php, os, variant):
    return dict(get_common_subst(), **dict({
            'PHP_ENV_DEFAULTS': get_env_defaults_str(php, os, variant),
            'PHP_ENV_SETTINGS': get_env_settings_str(php, os, variant),
            'DOCKER_FROM_TAG': get_tag(php, os, variant),
            'DOCKER_PHP_ARGS': get_docker_args_str(php, os, variant),
            'DOCKER_PHP_ENV': get_docker_env_str(php, os, variant)
        }, **get_params(php, os, variant)))


def get_global_subst():
    matrix = get_matrix()
    return dict(get_common_subst(), **dict({
            'MICROBADGES': get_microbadges_str(matrix),
            'CIRCLE_JOBS': get_circle_jobs_str(matrix),
            'CIRCLE_WORKFLOW_JOBS': get_circle_workflow_jobs_str(matrix)
        }))


def get_context(php, os, variant):
    return {'dir': get_context_dir(php, os, variant),
            'files': get_context_files(php, os, variant),
            'subst': get_context_subst(php, os, variant)}


def is_excluded(t):
    return len(set([t[:1], t[:2], t]) & set(exclusions())) > 0


def get_matrix():
    return [t for t in itertools.product(phps(), oses(), variants()) if not is_excluded(t)]


def get_contexts():
    return [get_context(php, os, variant) for (php, os, variant) in get_matrix()]


def phps():
    return [ '7.0', '7.1', '7.2', '7.3' ]


def oses():
    return [ 'jessie', 'stretch', 'buster' ]


def variants():
    return [ 'apache', 'cli' ]


def exclusions():
    return [
        ('7.0', 'stretch'),
        ('7.0', 'buster'),
        ('7.1', 'stretch'),
        ('7.1', 'buster'),
        ('7.2', 'jessie'),
        ('7.3', 'jessie'),
    ]

contexts = get_contexts()
files = { '.circleci/config.yml.in': '.circleci/config.yml',
          '.circleci/upload.in': '.circleci/upload',
          'README.md.in': 'README.md' }
subst = get_global_subst()
