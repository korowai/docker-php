#!/bin/sh

TPL=$(cat << 'EOF'
- [![](https://images.microbadger.com/badges/version/korowai/php:@TAG@.svg)](https://microbadger.com/images/korowai/php:@TAG@ "korowai/php:@TAG@")
  [![](https://images.microbadger.com/badges/image/korowai/php:@TAG@.svg)](https://microbadger.com/images/korowai/php:@TAG@ "Docker image size")
  [![](https://images.microbadger.com/badges/commit/korowai/php:@TAG@.svg)](https://microbadger.com/images/korowai/php:@TAG@ "Source code")
EOF
)

while IFS= read -r F; do
  if echo $F | grep -q '^\([a-z0-9\.-]\+\)$'; then
    echo "$TPL" | sed -e "s#@TAG@#$F#g";
  else
    echo $F;
  fi;
done
