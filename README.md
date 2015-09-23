# marketing-template-publisher

## Introduction

This project contains Python scripts for publishing wosai meijia marketing templates.

## Requirements
Make sure you have python installed on your machine. Minimum version tested is 2.7.10. Platform support is only tested on *nix systems.

## User Guide

1. Get template zip file and unzip it. It should contain a template folder and a mp3 file.
2. Copy make.py, publish.py and index.html to the template folder.
3. Run `python/python3 make.py -n/--name [template_name]`.
4. Copy generated folder to `yingxiao-fe/template/normal(festival)`.
5. Edit `yingxiao-fe/template/assets/js/edit.js`, add default template text. The default template text can be found in the .psd file that comes with the template.
6. Run `python/python3 publish.py --test` for testing.
7. Run `python/python3 publish.py --production` for release.