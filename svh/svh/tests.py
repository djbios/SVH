from django.test import TestCase


class Benchmarks(TestCase): #  not run in ./manage.py test (because of naming), but can be run manually

     def bench_hash(self):
        def hash_file(path):
            import hashlib
            BLOCKSIZE = 65536
            hasher = hashlib.md5()
            with open(path, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            return hasher.hexdigest()

        import os, time
        from imohash import hashfile
        GB = 1024 * 1024 * 1024  # 1GB
        path = '/tmp/large_file'
        with open(path, 'wb') as fout:
            fout.write(os.urandom(GB))

        start_time = time.time()
        hash_file(path)
        time1 = time.time() - start_time

        start_time = time.time()
        hashfile(path)
        time2 = time.time() - start_time

        print(time1, time2)
