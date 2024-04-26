# Copyright 2022 MosaicML Composer authors
# SPDX-License-Identifier: Apache-2.0

import time
from pathlib import Path

import pytest

from composer.utils import GCSObjectStore

__DUMMY_OBJ__ = '/tmp/dummy.ckpt'
__NUM_BYTES__ = 1000
bucket_name = 'mosaicml-composer-tests'


@pytest.mark.remote
@pytest.fixture
def gs_object_store():
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    remote_dir = 'gs://mosaicml-composer-tests/streaming/'
    yield GCSObjectStore(remote_dir)


@pytest.mark.remote
def test_bucket_not_found():
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    with pytest.raises(FileNotFoundError):
        # Add the necessary code here to complete the test case
        _ = GCSObjectStore('gs://not_a_bucket/streaming')


@pytest.mark.remote
    import gs_object_store  # Add the necessary import statement
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    object_name = 'test-object'
    expected_uri = 'gs://mosaicml-composer-tests/streaming/test-object'
    assert gs_object_store.get_uri(object_name) == expected_uri, "The URI retrieved from gs_object_store does not match the expected URI"


@pytest.mark.remote
def test_get_key(gs_object_store):
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    object_name = 'test-object'
    expected_key = 'streaming/test-object'
    assert (gs_object_store.get_key(object_name) == expected_key)


@pytest.mark.remote
    from pathlib import Path  # Add the necessary import statement for Path
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    fn = Path(__DUMMY_OBJ__)
    with open(fn, 'wb') as fp:
        fp.write(bytes('0' * __NUM_BYTES__, 'utf-8'))
    gs_object_store.upload_object(fn)
    # Add the necessary assertion or validation step here to complete the test case

    if result == 'success':
        assert (gs_object_store.get_object_size(__DUMMY_OBJ__) == __NUM_BYTES__)
    else:  # not found
        with pytest.raises(FileNotFoundError):
            gs_object_store.get_object_size(__DUMMY_OBJ__ + f'time.ctime()')


@pytest.mark.remote
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    from google.cloud.storage import Blob
    destination_blob_name = '/tmp/dummy.ckpt2'
    key = gs_object_store.get_key(destination_blob_name)  # Add the necessary import statement for gs_object_store
    stats = Blob(bucket=gs_object_store.bucket, name=key).exists(gs_object_store.client)
    if not stats:
        gs_object_store.upload_object(__DUMMY_OBJ__, destination_blob_name)  # Add the necessary validation step after upload
        gs_object_store.upload_object(__DUMMY_OBJ__, destination_blob_name)


@pytest.mark.remote
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    from google.cloud.storage import Blob
    destination_blob_name = '/tmp/dummy.ckpt2'
    key = gs_object_store.get_key(destination_blob_name)  # Add the necessary import statement for gs_object_store
    stats = Blob(bucket=gs_object_store.bucket, name=key).exists(gs_object_store.client)
    if not stats:
        gs_object_store.upload_object(__DUMMY_OBJ__, destination_blob_name)  # Add the necessary validation step after upload
        gs_object_store.upload_object(__DUMMY_OBJ__, destination_blob_name)
    objects = gs_object_store.list_objects()
    assert (key in objects)


@pytest.mark.remote
    from pathlib import Path  # Add the necessary import statement for Path
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    fn = Path(__DUMMY_OBJ__)
    with open(fn, 'wb') as fp:
        fp.write(bytes('0' * __NUM_BYTES__, 'utf-8'))
    gs_object_store.upload_object(fn)

    object_name = __DUMMY_OBJ__
    filename = './dummy.ckpt.download'
    # Add the necessary code for downloading the object and any validation steps after download

    if result == 'success':
        gs_object_store.download_object(object_name, filename, overwrite=True)

    elif result == 'file_exists':
        with pytest.raises(FileExistsError):
            gs_object_store.download_object(object_name, __DUMMY_OBJ__)
    else:  # obj_not_found
        with pytest.raises(FileNotFoundError):
            gs_object_store.download_object(object_name + f'{time.ctime()}', filename, overwrite=True)
