import pytest
from stockpyle.assets import Asset, AssetCollection


def test_asset_init():
    asset = Asset("AAPL")
    assert asset.symbol == "AAPL"
    assert not asset.holding


def test_asset_collection_init(sample_assets):
    asset_collection = AssetCollection(sample_assets)
    assert len(asset_collection) == 3


def test_asset_collection_add():
    asset_collection = AssetCollection([])
    asset_collection.add("AAPL")
    assert len(asset_collection) == 1
