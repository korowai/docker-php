#!/bin/bash -eu

versions="7.0 7.1 7.2";
suites="jessie stretch";
frontends="cli apache";

generated_warning() {
cat <<-EOH
#
# NOTE: FILE GENERATED VIA "update.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY
#
EOH
}

for version in $versions; do
  for suite in $suites; do
    [ -d "$version/$suite" ] || continue;
    for frontend in $frontends; do
      targetDir="$version/$suite/$frontend";
      [ -d  "$targetDir" ] || mkdir "$targetDir";
      targetFile="$targetDir/Dockerfile";
      dockerFromTag="${version}-${frontend}-${suite}";
      ( generated_warning ; cat Dockerfile.template ) | sed \
        -e "s:%%DOCKER_FROM_TAG%%:${dockerFromTag}:g" \
      > "${targetFile}"
    done
  done
done
