import pickle

# pickleに保存した.h5 .hdf5ファイルの読み込み
with open('shop_cnn', 'rb') as b:
    shop_cnn_weight = pickle.load(b)
