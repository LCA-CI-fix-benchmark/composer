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
    # Skip this test if the GCS service account is not configured on the CI node
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    with pytest.raises(FileNotFoundError):
        _ = GCSObjectStore('gs://not_a_bucket/streaming')


@pytest.mark.remote
def test_get_uri(gs_object_store):
    # Skip this test if the GCS service account is not configured on the CI node
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    object_name = 'test-object'
    expected_uri = 'gs://mosaicml-composer-tests/streaming/test-object'
    assert (gs_object_store.get_uri(object_name) == expected_uri)


@pytest.mark.remote
def test_get_key(gs_object_store):
    # Skip this test if the GCS service account is not configured on the CI node
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    object_name = 'test-object'
    expected_key = 'streaming/test-object'
    assert (gs_object_store.get_key(object_name) == expected_key)


@pytest.mark.remote
    fn = Path(__DUMMY_OBJ__)
    with open(fn, 'wb') as fp:
        fp.write(bytes('0' * __NUM_BYTES__, 'utf-8'))
    gs_object_store.upload_object(fn)

    if result == 'success':
        # Verify that the uploaded object size matches the expected number of bytes
        assert gs_object_store.get_object_size(__DUMMY_OBJ__) == __NUM_BYTES__

    if result == 'success':
        assert (gs_object_store.get_object_size(__DUMMY_OBJ__) == __NUM_BYTES__)
    else:  # not found
        with pytest.raises(FileNotFoundError):
            gs_object_store.get_object_size(__DUMMY_OBJ__ + f'time.ctime()')


@pytest.mark.remote
def test_upload_object(gs_object_store):
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    from google.cloud.storage import Blob
    destination_blob_name = '/tmp/dummy.ckpt2'
    key = gs_object_store.get_key(destination_blob_name)
    stats = Blob(bucket=gs_object_store.bucket, name=key).exists(gs_object_store.client)
    if not stats:
        gs_object_store.upload_object(__DUMMY_OBJ__, destination_blob_name)


@pytest.mark.remote
    key = gs_object_store.get_key(destination_blob_name)
    stats = Blob(bucket=gs_object_store.bucket, name=key).exists(gs_object_store.client)
    if not stats:
        gs_object_store.upload_object(__DUMMY_OBJ__, destination_blob_name)
    objects = gs_object_store.list_objects()
    
    # Verify that the key exists in the list of objects after uploading
    assert key in objects
    objects = gs_object_store.list_objects()
    assert (key in objects)


@pytest.mark.remote
@pytest.mark.parametrize('result', ['success', 'file_exists', 'obj_not_found'])
def test_download_object(gs_object_store, tmp_path, result: str):
    pytest.skip('Run this test suite only after GCS service account is configured on CI node.')
    fn = Path(__DUMMY_OBJ__)
    with open(fn, 'wb') as fp:
        fp.write(bytes('0' * __NUM_BYTES__, 'utf-8'))
    gs_object_store.upload_object(fn)

    object_name = __DUMMY_OBJ__
    filename = './dummy.ckpt.download'

    if result == 'success':
        gs_object_store.download_object(object_name, filename, overwrite=True)

    elif result == 'file_exists':
        with pytest.raises(FileExistsError):
            gs_object_store.download_object(object_name, __DUMMY_OBJ__)
    else:  # obj_not_found
        with pytest.raises(FileNotFoundError):
            gs_object_store.download_object(object_name + f'{time.ctime()}', filename, overwrite=True)
