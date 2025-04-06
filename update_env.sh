conda env export | sed '/^prefix: /d' > environment.yml
