import block
import random

class Stage:
    """
    テトリスの盤面を管理するクラスです。
    """
    WIDTH = 10  # 盤面の幅
    HEIGHT = 20 # 盤面の高さ

    NONE = 0    # 空マス
    BLOCK = 1   # ブロックマス
    FIX = 2     # 固定ブロックマス
    SHADOW = 3  # 影

    def __init__(self):
        """
        盤面を生成させます。
        """
        self.data = [[Stage.NONE for i in range(Stage.WIDTH)] for j in range(Stage.HEIGHT)]
#        self.data[0][0] = Stage.BLOCK
#        self.data[0][1] = Stage.FIX
        self.block = block.Block()
        self.shadow = block.Block()
        self.type = 0
        self.rot = 0
#        self.type = random.randint(0, 6)
#        self.rot = random.randint(0, 3)
        self.can_drop = True
        self.remove_line = [False for i in range(Stage.HEIGHT)]
        self.is_fix = False
        self.__select_block()

    def update(self):
        """
        ステージの更新処理を行うメソッドです。
        """
#        self.block.y += 10
        self.__marge_block()

        # もし下方向に衝突しない場合
        if not self.is_collision_bottom():
            self.is_fix = False
            if self.can_drop:
                self.__drop_block()
        # もし下方向に衝突する場合
        else:
            self.is_fix = True
            self.__fix_block()
            self.__check_remove_lines()
            self.__remove_lines()
            self.block.reset()
            self.__select_block()
            # self.block.y = -1
#            self.clear_check()

    def input(self, key):
        """
        キー入力を受け付けるメソッドです。
        各キーの入力に対しての処理を記述してください
        """
        if key == 'space':   # スペースキー
            self.can_drop = not self.can_drop

        if key == 'w':  # Wキー(回転)
            # print('wキーが押されました')
            self.__rotation_block()

        if key == 'a':  # Aキー(左移動)
            # print('aキーが押されました')
            if not self.is_collision_left():
                self.block.x -= 1

        if key == 's':  # Sキー(下移動)
            # print('sキーが押されました')
            self.hard_drop()

        if key == 'd':  # Dキー(右移動)
            # print('dキーが押されました')
            if not self.is_collision_right():
                self.block.x += 1

    def __select_block(self):
        """
        ブロックの種類と角度をランダムに選びます。
        """
        # ランダムにブロックの種類を選ぶ
        self.type = random.randint(0, block.Block.TYPE_MAX - 1)
        # ランダムにブロックの角度を選ぶ
        self.rot = random.randint(0, block.Block.ROT_MAX - 1)

    def __rotation_block(self):
        """
        ブロックを回転させるメソッドです。
        """
        """
        self.rot += 1
        if self.rot == block.Block.ROT_MAX
            self.rot = 0
        """
        if self.__can_rotation_block():
            self.rot = (self.rot + 1) % block.Block.ROT_MAX

    def __can_rotation_block(self):
        """
        現在のブロックが回転可能かを判定するメソッドです。
        回転することが出来るのであればTrueを返却し、
        そうでなければ、Falseを返却します。
        """

        # 次の角度
        n_rot = (self.rot + 1) % block.Block.ROT_MAX
        # ブロックの座標
        b_x = self.block.x
        b_y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 次の角度のブロック情報を取得する
                if self.block.get_cell_data(self.type, n_rot, j, i) == Stage.BLOCK:
                    # 範囲外チェック
                    if self.is_out_of_stage(b_x + j, b_y + i):
                        return False
                    # 固定ブロックとの衝突チェック
                    if self.data[b_y + i][b_x + j] == Stage.FIX:
                        return False
        return True


    def __drop_block(self):
        """
        ブロックを１段下げるメソッドです。
        """
        self.block.y += 1

    def __drop_shadow(self):
        """
        影を１段下げるメソッドです。
        """
        self.shadow.y += 1

    def __marge_block(self):
        """
        ステージのデータにブロックのデータをマージするメソッドです。
        """
        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot
        b_x = self.block.x
        b_y = self.block.y

        # ステージの状態を一度リセット
        for i in range(Stage.HEIGHT):
            for j in range(Stage.WIDTH):
                if self.data[i][j] == Stage.BLOCK:
                    self.data[i][j] = Stage.NONE

        # ブロックデータをステージに反映
        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    if not self.is_out_of_stage(b_x + j, b_y + i):
                        self.data[b_y + i][b_x + j] = Stage.BLOCK

    def __fix_block(self):
        """
        ブロックを固定するメソッドです。
        """

        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot
        b_x = self.block.x
        b_y = self.block.y

        x = self.block.x
        y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    self.data[b_y + i][b_x + j] = Stage.FIX

    def is_out_of_stage(self, x, y):
        """
        指定されたステージの座標が範囲外かを調べるメソッドです。
        x: ステージセルのＸ軸
        y: ステージセルのＹ軸
        """

        return x < 0 or x >=Stage.WIDTH or y < 0 or y >= Stage.HEIGHT

    def is_collision_bottom(self, x=-1, y=-1):
        """
        下方向の衝突判定を行うメソッドです。
        衝突していればTrueが返却され、そうでなければFalseが返却されます。
        x: 対象のブロックのX軸座標
        y: 対象のブロックのY軸座標
        """

        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot
#        b_x = self.block.x
#        b_y = self.block.y

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ下げたマスが
                    # ステージの範囲外だった場合
                    tx = x + j
                    ty = y + i + 1
                    if self.is_out_of_stage(tx, ty):
                        return True
                    # 対象のブロックマスの位置から１つ下げたマスが
                    # 固定されたブロックのマス(2)だった場合
                    if self.data[y+i+1][x+j] == Stage.FIX:
                        return True

        # どの条件にも当てはまらない場合は常にどこにも衝突していなくぃ
        return False


    def is_collision_left(self, x=-1, y=-1):
        """
        左方向の衝突判定を行うメソッドです。
        衝突していればTrueが返却され、そうでなければFalseが返却されます。
        x: 対象のブロックのX軸座標
        y: 対象のブロックのY軸座標
        """

        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot

#        b_x = self.block.x
#        b_y = self.block.y

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ左のマスが
                    # ステージの範囲外だった場合
                    if self.is_out_of_stage(x + j - 1, y + i):
                        return True
                    # 対象のブロックマスの位置から１つ左のマスが
                    # 固定されたブロックのマス(2)だった場合
                    if self.data[y+i][x+j-1] == Stage.FIX:
                        return True

        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False


    def is_collision_right(self, x=-1, y=-1):
        """
        右方向の衝突判定を行うメソッドです。
        衝突していればTrueが返却され、そうでなければFalseが返却されます。
        x: 対象のブロックのX軸座標
        y: 対象のブロックのY軸座標
        """

#        b_x = self.block.x
#        b_y = self.block.y
        b_t = self.type
        b_r = self.rot
#        b_t = self.block.type
#        b_r = self.block.rot

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ右のマスが
                    # ステージの範囲外だった場合
                    if self.is_out_of_stage(x + j + 1, y + i):
                        return True
                    # 対象のブロックマスの位置から１つ右のマスが
                    # 固定されたブロックのマス(2)だった場合
                    if self.data[y+i][x+j+1] == Stage.FIX:
                        return True

        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def hard_drop(self):
        """
        ハードドロップ処理です。
        """
        # 下に衝突判定がない限りブロックを下げ続ける
        while True:
            if not self.is_collision_bottom():
 #               self.block.y += 1
                self.__drop_block()
            else:
                break

    def make_shadow(self):
        """
        影を作る処理です。
        """
        # 下に衝突判定がない限りブロックを下げ続ける
        while True:
            if not self.is_collision_bottom():
                self.__drop_block()
            else:
                break


    def __check_remove_lines(self):
        """
        消える列をチェックするメソッドです。
        """
        for i in range(Stage.HEIGHT):
            flg = True
            for j in range(Stage.WIDTH):
                if self.data[i][j] != Stage.FIX:
                    flg = False
                    break
            self.remove_line[i] = flg


    def __remove_lines(self):
        """
        列を消すメソッドです。
        """

        # 置き換え先の列を参照するポインタ
        idx = Stage.HEIGHT-1

        # 揃っている列の削除(NONEにする)
        for i in range(Stage.HEIGHT):
            if self.remove_line[i]:
                for j in range(Stage.WIDTH):
                    self.data[i][j] = Stage.NONE

        # 揃っていない列を下の列から積み上げなおす
        for i in reversed(range(Stage.HEIGHT)):
            # もし、対象の列が揃っていなかった場合
            if not self.remove_line[i]:
                for j in range(Stage.WIDTH):
                    # 置き換え先の列に揃っていない列を代入する
#DBG                    print('i={}, j={}, cnt={}'.format(i, j, cnt))
                    self.data[idx][j] = self.data[i][j]
                # 置き換え先の列を参照するポインタを１列上げる
                idx -= 1

    def shadow_position(self):
        """
        テトリミノの影を作るｙ軸座標を計算してそのｙ軸座標を返却します。
        """
        # 現在のブロックの座標を退避
        tx = self.block.x
        ty = self.block.y

        while not self.is_collision_bottom(tx, ty):
            ty += 1

        return ty


    def is_end(self):
        """
        テトリスのゲームオーバー判定を行うメソッドです。
        ゲームオーバーであればTrueを返却し、
        そうでなければFalseを返却します。
        """

        # ブロックの情報を取得
        t = self.type
        r = self.rot
        x = self.block.x
        y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                cell_data = self.block.get_cell_data(t, r, j, i)
                if cell_data == Stage.BLOCK:
                    # 範囲外チェック
                    if not self.is_out_of_stage(x + j, y + i):
                        # 衝突チェック
                        if self.data[y + i][x + j] == Stage.FIX:
                            return True
        return False




"""
    def clear_check(self):
        b_t = self.type
        b_r = self.rot

        for i in range(Stage.HEIGHT):
            cnt = 0
            for j in range(Stage.WIDTH):
                if self.data[i][j] != Stage.FIX:
                    continue
                else:
                    cnt += 1

            if cnt == Stage.WIDTH:
                self.space_drop(i)
                i -= 1
                break


    def space_drop(self, line):
        for i in range(Stage.HEIGHT):
            if i < line:
                continue

            for j in range(Stage.WIDTH):
                if i == 0:
                    self.data[i][j] = Stage.NONE
                else:
                    self.data[i][j] = self.data[i-1][j]
"""



