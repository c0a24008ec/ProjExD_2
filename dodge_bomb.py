import os
import sys
import pygame as pg
import random as rd
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct):
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True #初期値は画面内
    if rct.left < 0 or WIDTH < rct.right: #横座標チェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦座標チェック
        tate = False
    return yoko, tate

# ゲームオーバー画面の表示
def gameover(screen: pg.Surface,) -> None: 
    """
    背景、文字、画像をロード
    関数が読み込まれたらゲームオーバー画面を表示
    """
    gg_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(gg_img, (0,0,0),(0,0,WIDTH,HEIGHT))
    gg_img.set_alpha(200)
    gg_rct = gg_img.get_rect()
    gg_rct.center = (WIDTH // 2, HEIGHT // 2)
    kk_gg_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_gg_rct1 = kk_gg_img.get_rect()
    kk_gg_rct2 = kk_gg_img.get_rect()
    kk_gg_rct1.center = (320, HEIGHT // 2)
    kk_gg_rct2.center = (800, HEIGHT // 2)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GAME OVER", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH // 2, HEIGHT // 2)     
    screen.blit(gg_img,gg_rct)
    screen.blit(txt, txt_rct)
    screen.blit(kk_gg_img, kk_gg_rct1)
    screen.blit(kk_gg_img, kk_gg_rct2)
    pg.display.update()
    time.sleep(5)
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_accs,bb_imgs = [], []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        bb_accs.append(r)
    return bb_imgs, bb_accs
def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    こうかとんの画像をsum_mvに応じて回転させて返す
    引数：sum_mv: こうかとんの移動量のタプル
    戻り値：回転させたこうかとんの画像
    """
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    kk_flip_img = pg.transform.flip(kk_img, True, False)  # こうかとんの画像を左右反
    kk_flip_rct = kk_flip_img.get_rect()
    kk_flip_rct.center = 300, 200
    loto_img = {
        (0, 0): pg.transform.rotozoom(kk_flip_img, 0, 1),
        (0, -5): pg.transform.rotozoom(kk_flip_img, 90, 1),
        (+5, -5): pg.transform.rotozoom(kk_flip_img, 45, 1),
        (+5, 0): pg.transform.rotozoom(kk_flip_img, 0, 1),
        (+5, +5): pg.transform.rotozoom(kk_flip_img, -45, 1),
        (0, +5): pg.transform.rotozoom(kk_flip_img, -90, 1),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1),
    }
    return loto_img[sum_mv]
def calc_orientation(org: pg.Rect, dst: pg.Rect,current_xy: list[float, float]) -> tuple[float, float]:
    """
    爆弾とこうかとんの位置を比較して、爆弾の移動方向を計算する
    引数：org: こうかとんのRect, dst: 爆弾のRect, current_xy: 現在の爆弾の移動方向
    戻り値：爆弾の移動方向のタプル(dx, dy)
    """
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    length = (dx**2 + dy**2)**0.5
    if length >= 300:
        nor_dx = dx * 50**0.5 / length
        nor_dy = dy * 50**0.5 / length
        return (nor_dx, nor_dy)
    else:
        return current_xy

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    clock = pg.time.Clock()
    tmr = 0
    DELTA = { # 移動量辞書
        pg.K_UP:(0,-5),
        pg.K_DOWN:(0,+5),
        pg.K_LEFT:(-5,0),
        pg.K_RIGHT:(+5,0)
    }
    
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = rd.randint(0,WIDTH)
    bb_rct.centery = rd.randint(0,HEIGHT)
    vx, vy = +5, +5
    
    
    
            

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        kk_img = get_kk_img(tuple(sum_mv))
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
