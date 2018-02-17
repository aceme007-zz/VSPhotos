# VSPhotos

exiv2 is being used to insert metadata into all photos.
It's open source and has a wide online community for any help
http://www.exiv2.org/

Have kept the tar just in case we need to find the exact version used
It unzips to /dist folder

src has all the folders which would be our input source dir for all images
```
(vs-venv) kkaul@kkaul-mac ~/Documents/VSPhotos (master) $ ls -lrt src/
total 0
drwxr-xr-x  152 kkaul  staff  4864 Feb 13 21:20 2013-10
```

vs-env is the python virtual env which I have created for all env vars
```
virtualenv vs-env
source vs-env/bin/activate
```

In case your IDE fails to find the env var, you can set it in your run configuration
I've added it in my virtual env
```
export DYLD_LIBRARY_PATH=/Users/kkaul/Documents/VSPhotos/dist/macosx/lib
```

