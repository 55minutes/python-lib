import zipfile, os

def zipDir( directory, zipFile ):
    """Zip an entire directory to a zip file."""
    directory = os.path.normpath(os.path.normcase(directory))
    z = zipfile.ZipFile( zipFile, 'w', compression=zipfile.ZIP_DEFLATED )

    for root, dirs, files in os.walk(directory):
        for f in files:
            f = os.path.normpath(os.path.normcase(os.path.join( root, f )))
            archiveName = f[len(os.path.commonprefix( (directory, f) ))+1:]
            z.write( f, archiveName, zipfile.ZIP_DEFLATED )

    z.close()

if __name__ == "__main__":
    zipDir( r'E:\dgs\media\dgs\temp\tmpnged65', r'E:\dgs\media\dgs\temp\test.zip' )