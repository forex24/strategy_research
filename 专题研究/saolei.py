import time
import numpy as np
import os
from PIL import ImageGrab, Image, ImageDraw, ImageFont
from sklearn.ensemble import RandomForestClassifier

import pyautogui as pag
from pynput.mouse import Listener

class Operator():
    def __init__(self):
        self.data_dir = './Computer Vision/data/saolei/'
        self._init_data_dir()
        
        self.lei_rect, self.block_size = self._confirm_lei_rect()
        self.j_rect = self._confirm_j_rect()

        self.j_labels = ['not ovr', 'ovr']
        self.lei_labels = ['closed', 'opened', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        self.j_cls_model = None
        self.lei_cls_model = None
    
    def _init_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _confirm_lei_rect(self):
        """ 确认 lei_rect, j_rect 的截图框位置 """
        def on_click(x, y, button, is_press):
            print(f"鼠标{button}键在({x}, {y})处{'按下'}")
            return False

        print('请点击雷区左上角')
        with Listener(on_click=on_click) as listener:
            listener.join()
        lei_lt = pag.position()  # 返回鼠标的坐标
        time.sleep(1)

        print('请点击雷区右下角')
        with Listener(on_click=on_click) as listener:
            listener.join()
        lei_rd = pag.position()  # 返回鼠标的坐标
        time.sleep(1)

        block_x = int(input('请输入雷区每行有多少block'))
        block_y = int(input('请输入雷区每列有多少block'))

        lei_rect = (lei_lt[0], lei_lt[1], lei_rd[0], lei_rd[1])
        block_size = (block_x, block_y)
        return lei_rect, block_size

    def _confirm_j_rect(self):
        def on_click(x, y, button, is_press):
            print(f"鼠标{button}键在({x}, {y})处{'按下'}")
            return False

        print('请点击判断结束区域左上角')
        with Listener(on_click=on_click) as listener:
            listener.join()
        j_lt = pag.position()  # 返回鼠标的坐标
        time.sleep(1)

        print('请点击判断结束区域右下角')
        with Listener(on_click=on_click) as listener:
            listener.join()
        j_rd = pag.position()  # 返回鼠标的坐标

        j_rect = (j_lt[0], j_lt[1], j_rd[0], j_rd[1])
        return j_rect

    def img_check(self, file_name):
        return os.path.exists(self.data_dir + file_name + '.jpg')

    def img_load(self, file_name):
        img = Image.open(self.data_dir + file_name + '.jpg')
        return img

    def img_save(self, img, file_name):
        """ 保存img到self.data_dir """
        img.save(self.data_dir + file_name + '.jpg')
        return True

    def screen_shot(self, rect, file_name=None):
        """ 根据rect进行截图，并保存本地 """
        img = ImageGrab.grab().crop(rect)
        if file_name:
            self.img_save(img, file_name)
        return img

    def get_block_img_arr(self, img, block_size, is_save=False):
        """ 根据输入的雷区图片，图片左上、右下坐标，图片的行列元素数，分割得到block_img_arr
            :param img:
            :param block_size:
            :return block_img_arr:
        """
        # 计算单元格长宽
        block_x, block_y = block_size
        w, h = img.size
        block_w, block_h = w/block_x, h/block_y

        # 对雷区进行单元分割， 获取block_img_arr
        block_img_arr = [[0 for _ in range(block_x)] for _ in range(block_y)]
        for x in range(block_x):
            for y in range(block_y):
                x1, y1 = x * block_w, y * block_h
                x2, y2 = x1 + block_w, y1 + block_h
                crop_img = img.crop((x1, y1, x2, y2))
                block_img_arr[y][x] = crop_img
                if is_save:
                    self.img_save(crop_img, 'lei_{}_{}'.format(y, x))
        return block_img_arr

    def gen_train_img(self, filename, loc=None):
        """ 实时截图获取训练数据 """
        if filename == 'ovr':
            img = self.screen_shot(self.j_rect, filename)
        elif filename == 'not ovr':
            img = self.screen_shot(self.j_rect, filename)
        elif filename in self.lei_labels:
            if loc is not None:
                lei_img = self.screen_shot(self.lei_rect)
                block_img_arr = self.get_block_img_arr(lei_img, self.block_size)
                x, y = loc
                img = block_img_arr[x][y]
                self.img_save(img, filename)
        elif filename == 'leiqu':
            lei_img = self.screen_shot(self.lei_rect)
            self.get_block_img_arr(lei_img, self.block_size, is_save=True)
        elif filename == '1-9':
            self.gen_1_9_img()
        return img
        
        
    def gen_1_9_img(self):
        """ 根据已经保存的 opened.jpg 补充生成1-9的图片 """
        if not self.img_check('opened'):
            print('未找到Pic->opened，请自行命名一个opened的图片作为基准图')
            return
        for num in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if not self.img_check(num):
                print('Gen {} Pic ~'.format(num))
                img = self.img_load('opened')
                img_size = img.size
                # 确定添加数字的位置
                l_dist, u_dist = (img_size[0] - 4) // 2, 1
                font_size = img_size[1] - 2
                font = ImageFont.truetype('simsun.ttc', font_size)
                add_number = ImageDraw.Draw(img)
                add_number.text((l_dist, u_dist), str(num), font=font, fill='black')
                self.img_save(img, num)
            else:
                print('{} Pic Exist~'.format(num))

    def _trans_img_2_fea_arr(self, img):
        """
            1. 将img转黑白图
            2. 生成 【横向+纵向】X【标准差 + 蜂度 + 偏度】共 6个值的特征序列
        """
        bw_img = img.convert('1')
        bw_img_arr = np.array(bw_img)

        # 横向
        h_arr_sum = bw_img_arr.sum(axis=1)
        h_mean, h_var = h_arr_sum.mean(), h_arr_sum.var()
        h_sc = ((h_arr_sum - h_mean)**3).mean()
        h_ku = ((h_arr_sum - h_mean)**4).mean()/pow(h_var, 2)

        # 纵向
        v_arr_sum = bw_img_arr.sum(axis=0)
        v_mean, v_var = v_arr_sum.mean(), v_arr_sum.var()
        v_sc = ((v_arr_sum - v_mean) ** 3).mean()
        v_ku = ((v_arr_sum - v_mean) ** 4).mean() / pow(v_var, 2)
        return np.array([h_var, h_sc, h_ku, v_var, v_sc, v_ku])

    def train_cls_model(self, label_type):
        """ 根据label_type加载训练图片，生成特征训练RandomForestClassifier模型 """
        if label_type == 'lei':
            labels = self.lei_labels
        elif label_type == 'j':
            labels = self.j_labels

        rf_cls = RandomForestClassifier()
        imgs = [self.img_load(img) for img in labels]
        features = np.array([self._trans_img_2_fea_arr(img) for img in imgs])
        rf_cls.fit(features, np.arange(len(labels)))
        return rf_cls

    def predict(self, img, label_type):
        """ 根据label_type，选择对应分类模型进行结果预测，如果模型不存在则训练一个 """
        assert label_type in ('lei', 'j'), print('请确保label_type in ("lei","j")')
        if label_type == 'lei':
            if self.lei_cls_model is None:
                self.lei_cls_model = self.train_cls_model(label_type)
            cls_model = self.lei_cls_model
            labels = self.lei_labels
        elif label_type == 'j':
            if self.j_cls_model is None:
                self.j_cls_model = self.train_cls_model(label_type)
            cls_model = self.j_cls_model
            labels = self.j_labels

        features = np.array([self._trans_img_2_fea_arr(img)])
        label_idx = cls_model.predict(features)[0]
        return labels[label_idx]