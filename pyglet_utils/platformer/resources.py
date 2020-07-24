from __future__ import annotations
from typing import List
import pyglet
from pyglet.image import Animation

pyglet.resource.path = ["/home/clayton/Pictures/sprites/platformer"]
pyglet.resource.reindex()

class ResourceImage:
    def __init__(self, path: str):
        self.path = path
        self.img = pyglet.resource.image(self.path)
    
    # def get_transform(self, *args, **kwargs) -> ResourceImage:
    #     self.img = self.img.get_transform(args, kwargs)
    #     return self
    
    def copy(self) -> ResourceImage:
        new_res_img = ResourceImage(path=self.path)
        new_res_img.img = self.img
        return new_res_img

    def to_dict(self) -> dict:
        return {
            'resource_type': 'image',
            'path': self.path
        }
    
    @classmethod
    def from_dict(self, item_dict: dict) -> ResourceImage:
        return ResourceImage(
            path=item_dict['path']
        )

class ResourceAnimation:
    def __init__(self, res_img_path_seq: List[ResourceImage], duration: float=1/20, loop: bool=True):
        self.path_seq = [res.path for res in res_img_path_seq]
        self.duration = duration
        self.loop = loop
        self.animation = Animation.from_image_sequence(sequence=[res.img for res in res_img_path_seq], duration=self.duration, loop=self.loop)

    def to_dict(self) -> dict:
        return {
            'resource_type': 'animation',
            'path_seq': self.path_seq,
            'duration': self.duration,
            'loop': self.loop
        }
    
    @classmethod
    def from_dict(self, item_dict: dict) -> ResourceAnimation:
        return ResourceAnimation(
            res_img_path_seq=[ResourceImage(path) for path in item_dict['path_seq']],
            duration=item_dict['duration'],
            loop=item_dict['loop']
        )

class EnemyImages:
    blockerBody = ResourceImage("Enemies/blockerBody.png")
    blockerMad = ResourceImage("Enemies/blockerMad.png")
    blockerSad = ResourceImage("Enemies/blockerSad.png")
    enemies_spritesheet = ResourceImage("Enemies/enemies_spritesheet.png")
    fishDead = ResourceImage("Enemies/fishDead.png")
    fishSwim1 = ResourceImage("Enemies/fishSwim1.png")
    fishSwim2 = ResourceImage("Enemies/fishSwim2.png")
    flyDead = ResourceImage("Enemies/flyDead.png")
    flyFly1 = ResourceImage("Enemies/flyFly1.png")
    flyFly2 = ResourceImage("Enemies/flyFly2.png")
    pokerMad = ResourceImage("Enemies/pokerMad.png")
    pokerSad = ResourceImage("Enemies/pokerSad.png")
    slimeDead = ResourceImage("Enemies/slimeDead.png")
    slimeWalk1 = ResourceImage("Enemies/slimeWalk1.png")
    slimeWalk2 = ResourceImage("Enemies/slimeWalk2.png")
    snailShell = ResourceImage("Enemies/snailShell.png")
    snailShell_upsidedown = ResourceImage("Enemies/snailShell_upsidedown.png")
    snailWalk1 = ResourceImage("Enemies/snailWalk1.png")
    snailWalk2 = ResourceImage("Enemies/snailWalk2.png")

class HUDImages:
    hud_0 = ResourceImage("HUD/hud_0.png")
    hud_1 = ResourceImage("HUD/hud_1.png")
    hud_2 = ResourceImage("HUD/hud_2.png")
    hud_3 = ResourceImage("HUD/hud_3.png")
    hud_4 = ResourceImage("HUD/hud_4.png")
    hud_5 = ResourceImage("HUD/hud_5.png")
    hud_6 = ResourceImage("HUD/hud_6.png")
    hud_7 = ResourceImage("HUD/hud_7.png")
    hud_8 = ResourceImage("HUD/hud_8.png")
    hud_9 = ResourceImage("HUD/hud_9.png")
    hud_coins = ResourceImage("HUD/hud_coins.png")
    hud_gem_blue = ResourceImage("HUD/hud_gem_blue.png")
    hud_gem_green = ResourceImage("HUD/hud_gem_green.png")
    hud_gem_red = ResourceImage("HUD/hud_gem_red.png")
    hud_gem_yellow = ResourceImage("HUD/hud_gem_yellow.png")
    hud_heartEmpty = ResourceImage("HUD/hud_heartEmpty.png")
    hud_heartFull = ResourceImage("HUD/hud_heartFull.png")
    hud_heartHalf = ResourceImage("HUD/hud_heartHalf.png")
    hud_keyBlue_disabled = ResourceImage("HUD/hud_keyBlue_disabled.png")
    hud_keyBlue = ResourceImage("HUD/hud_keyBlue.png")
    hud_keyGreem_disabled = ResourceImage("HUD/hud_keyGreem_disabled.png")
    hud_keyGreen = ResourceImage("HUD/hud_keyGreen.png")
    hud_keyRed_disabled = ResourceImage("HUD/hud_keyRed_disabled.png")
    hud_keyRed = ResourceImage("HUD/hud_keyRed.png")
    hud_keyYellow_disabled = ResourceImage("HUD/hud_keyYellow_disabled.png")
    hud_keyYellow = ResourceImage("HUD/hud_keyYellow.png")
    hud_p1Alt = ResourceImage("HUD/hud_p1Alt.png")
    hud_p1 = ResourceImage("HUD/hud_p1.png")
    hud_p2Alt = ResourceImage("HUD/hud_p2Alt.png")
    hud_p2 = ResourceImage("HUD/hud_p2.png")
    hud_p3Alt = ResourceImage("HUD/hud_p3Alt.png")
    hud_p3 = ResourceImage("HUD/hud_p3.png")
    hud_spritesheet = ResourceImage("HUD/hud_spritesheet.png")
    hud_x = ResourceImage("HUD/hud_x.png")

class ItemImages:
    bombFlash = ResourceImage("Items/bombFlash.png")
    bomb = ResourceImage("Items/bomb.png")
    bush = ResourceImage("Items/bush.png")
    buttonBlue = ResourceImage("Items/buttonBlue.png")
    buttonBlue_pressed = ResourceImage("Items/buttonBlue_pressed.png")
    buttonGreen = ResourceImage("Items/buttonGreen.png")
    buttonGreen_pressed = ResourceImage("Items/buttonGreen_pressed.png")
    buttonRed = ResourceImage("Items/buttonRed.png")
    buttonRed_pressed = ResourceImage("Items/buttonRed_pressed.png")
    buttonYellow = ResourceImage("Items/buttonYellow.png")
    buttonYellow_pressed = ResourceImage("Items/buttonYellow_pressed.png")
    cactus = ResourceImage("Items/cactus.png")
    chain = ResourceImage("Items/chain.png")
    cloud1 = ResourceImage("Items/cloud1.png")
    cloud2 = ResourceImage("Items/cloud2.png")
    cloud3 = ResourceImage("Items/cloud3.png")
    coinBronze = ResourceImage("Items/coinBronze.png")
    coinGold = ResourceImage("Items/coinGold.png")
    coinSilver = ResourceImage("Items/coinSilver.png")
    fireball = ResourceImage("Items/fireball.png")
    flagBlue2 = ResourceImage("Items/flagBlue2.png")
    flagBlueHanging = ResourceImage("Items/flagBlueHanging.png")
    flagBlue = ResourceImage("Items/flagBlue.png")
    flagGreen2 = ResourceImage("Items/flagGreen2.png")
    flagGreenHanging = ResourceImage("Items/flagGreenHanging.png")
    flagGreen = ResourceImage("Items/flagGreen.png")
    flagRed2 = ResourceImage("Items/flagRed2.png")
    flagRedHanging = ResourceImage("Items/flagRedHanging.png")
    flagRed = ResourceImage("Items/flagRed.png")
    flagYellow2 = ResourceImage("Items/flagYellow2.png")
    flagYellowHanging = ResourceImage("Items/flagYellowHanging.png")
    flagYellow = ResourceImage("Items/flagYellow.png")
    gemBlue = ResourceImage("Items/gemBlue.png")
    gemGreen = ResourceImage("Items/gemGreen.png")
    gemRed = ResourceImage("Items/gemRed.png")
    gemYellow = ResourceImage("Items/gemYellow.png")
    items_spritesheet = ResourceImage("Items/items_spritesheet.png")
    keyBlue = ResourceImage("Items/keyBlue.png")
    keyGreen = ResourceImage("Items/keyGreen.png")
    keyRed = ResourceImage("Items/keyRed.png")
    keyYellow = ResourceImage("Items/keyYellow.png")
    mushroomBrown = ResourceImage("Items/mushroomBrown.png")
    mushroomRed = ResourceImage("Items/mushroomRed.png")
    particleBrick1a = ResourceImage("Items/particleBrick1a.png")
    particleBrick1b = ResourceImage("Items/particleBrick1b.png")
    particleBrick2a = ResourceImage("Items/particleBrick2a.png")
    particleBrick2b = ResourceImage("Items/particleBrick2b.png")
    plant = ResourceImage("Items/plant.png")
    plantPurple = ResourceImage("Items/plantPurple.png")
    rock = ResourceImage("Items/rock.png")
    snowhill = ResourceImage("Items/snowhill.png")
    spikes = ResourceImage("Items/spikes.png")
    springboardDown = ResourceImage("Items/springboardDown.png")
    springboardUp = ResourceImage("Items/springboardUp.png")
    star = ResourceImage("Items/star.png")
    switchLeft = ResourceImage("Items/switchLeft.png")
    switchMid = ResourceImage("Items/switchMid.png")
    switchRight = ResourceImage("Items/switchRight.png")
    weightChained = ResourceImage("Items/weightChained.png")
    weight = ResourceImage("Items/weight.png")

class PlayerImages:
    class p1:
        duck = ResourceImage("Player/p1_duck.png")
        front = ResourceImage("Player/p1_front.png")
        hurt = ResourceImage("Player/p1_hurt.png")
        jump = ResourceImage("Player/p1_jump.png")
        spritesheet = ResourceImage("Player/p1_spritesheet.png")
        stand = ResourceImage("Player/p1_stand.png")
        walk = ResourceImage("Player/p1_walk/p1_walk.png")
        walk01 = ResourceImage("Player/p1_walk/PNG/p1_walk01.png")
        walk02 = ResourceImage("Player/p1_walk/PNG/p1_walk02.png")
        walk03 = ResourceImage("Player/p1_walk/PNG/p1_walk03.png")
        walk04 = ResourceImage("Player/p1_walk/PNG/p1_walk04.png")
        walk05 = ResourceImage("Player/p1_walk/PNG/p1_walk05.png")
        walk06 = ResourceImage("Player/p1_walk/PNG/p1_walk06.png")
        walk07 = ResourceImage("Player/p1_walk/PNG/p1_walk07.png")
        walk08 = ResourceImage("Player/p1_walk/PNG/p1_walk08.png")
        walk09 = ResourceImage("Player/p1_walk/PNG/p1_walk09.png")
        walk10 = ResourceImage("Player/p1_walk/PNG/p1_walk10.png")
        walk11 = ResourceImage("Player/p1_walk/PNG/p1_walk11.png")
        walk_seq = [
            walk01, walk02, walk03, walk04, walk05, walk06, walk07,
            walk08, walk09, walk10, walk11
        ]

        # Need to change anchor position to center so that the player doesn't move when flipped
        for res in walk_seq + [stand, jump]:
            res.img.anchor_x = res.img.width // 2
        
        walk_right_seq = [res_img.copy() for res_img in walk_seq]
        for res_img in walk_right_seq:
            res_img.img = res_img.img.get_transform(flip_x=False)
        walk_left_seq = [res_img.copy() for res_img in walk_seq]
        for res_img in walk_left_seq:
            res_img.img = res_img.img.get_transform(flip_x=True)
        idle_right = stand.copy()
        idle_right.img = idle_right.img.get_transform(flip_x=False)
        idle_left = stand.copy()
        idle_left.img = idle_left.img.get_transform(flip_x=True)
        jump_right = jump.copy()
        jump_right.img = jump_right.img.get_transform(flip_x=False)
        jump_left = jump.copy()
        jump_left.img = jump_left.img.get_transform(flip_x=True)

        walk_right_anim = ResourceAnimation(res_img_path_seq=walk_right_seq, duration=1/20, loop=True)
        walk_left_anim = ResourceAnimation(res_img_path_seq=walk_left_seq, duration=1/20, loop=True)

    class p2:
        duck = ResourceImage("Player/p2_duck.png")
        front = ResourceImage("Player/p2_front.png")
        hurt = ResourceImage("Player/p2_hurt.png")
        jump = ResourceImage("Player/p2_jump.png")
        spritesheet = ResourceImage("Player/p2_spritesheet.png")
        stand = ResourceImage("Player/p2_stand.png")
        walk = ResourceImage("Player/p2_walk/p2_walk.png")
        walk01 = ResourceImage("Player/p2_walk/PNG/p2_walk01.png")
        walk02 = ResourceImage("Player/p2_walk/PNG/p2_walk02.png")
        walk03 = ResourceImage("Player/p2_walk/PNG/p2_walk03.png")
        walk04 = ResourceImage("Player/p2_walk/PNG/p2_walk04.png")
        walk05 = ResourceImage("Player/p2_walk/PNG/p2_walk05.png")
        walk06 = ResourceImage("Player/p2_walk/PNG/p2_walk06.png")
        walk07 = ResourceImage("Player/p2_walk/PNG/p2_walk07.png")
        walk08 = ResourceImage("Player/p2_walk/PNG/p2_walk08.png")
        walk09 = ResourceImage("Player/p2_walk/PNG/p2_walk09.png")
        walk10 = ResourceImage("Player/p2_walk/PNG/p2_walk10.png")
        walk11 = ResourceImage("Player/p2_walk/PNG/p2_walk11.png")
        walk_seq = [
            walk01, walk02, walk03, walk04, walk05, walk06, walk07,
            walk08, walk09, walk10, walk11
        ]

        # Need to change anchor position to center so that the player doesn't move when flipped
        for res in walk_seq + [stand, jump]:
            res.img.anchor_x = res.img.width // 2
        
        walk_right_seq = [res_img.copy() for res_img in walk_seq]
        for res_img in walk_right_seq:
            res_img.img = res_img.img.get_transform(flip_x=False)
        walk_left_seq = [res_img.copy() for res_img in walk_seq]
        for res_img in walk_left_seq:
            res_img.img = res_img.img.get_transform(flip_x=True)
        idle_right = stand.copy()
        idle_right.img = idle_right.img.get_transform(flip_x=False)
        idle_left = stand.copy()
        idle_left.img = idle_left.img.get_transform(flip_x=True)
        jump_right = jump.copy()
        jump_right.img = jump_right.img.get_transform(flip_x=False)
        jump_left = jump.copy()
        jump_left.img = jump_left.img.get_transform(flip_x=True)

        walk_right_anim = ResourceAnimation(res_img_path_seq=walk_right_seq, duration=1/20, loop=True)
        walk_left_anim = ResourceAnimation(res_img_path_seq=walk_left_seq, duration=1/20, loop=True)

    class p3:
        duck = ResourceImage("Player/p3_duck.png")
        front = ResourceImage("Player/p3_front.png")
        hurt = ResourceImage("Player/p3_hurt.png")
        jump = ResourceImage("Player/p3_jump.png")
        spritesheet = ResourceImage("Player/p3_spritesheet.png")
        stand = ResourceImage("Player/p3_stand.png")
        walk = ResourceImage("Player/p3_walk/p3_walk.png")
        walk01 = ResourceImage("Player/p3_walk/PNG/p3_walk01.png")
        walk02 = ResourceImage("Player/p3_walk/PNG/p3_walk02.png")
        walk03 = ResourceImage("Player/p3_walk/PNG/p3_walk03.png")
        walk04 = ResourceImage("Player/p3_walk/PNG/p3_walk04.png")
        walk05 = ResourceImage("Player/p3_walk/PNG/p3_walk05.png")
        walk06 = ResourceImage("Player/p3_walk/PNG/p3_walk06.png")
        walk07 = ResourceImage("Player/p3_walk/PNG/p3_walk07.png")
        walk08 = ResourceImage("Player/p3_walk/PNG/p3_walk08.png")
        walk09 = ResourceImage("Player/p3_walk/PNG/p3_walk09.png")
        walk10 = ResourceImage("Player/p3_walk/PNG/p3_walk10.png")
        walk11 = ResourceImage("Player/p3_walk/PNG/p3_walk11.png")
        walk_seq = [
            walk01, walk02, walk03, walk04, walk05, walk06, walk07,
            walk08, walk09, walk10, walk11
        ]

        # Need to change anchor position to center so that the player doesn't move when flipped
        for res in walk_seq + [stand, jump]:
            res.img.anchor_x = res.img.width // 2
        
        walk_right_seq = [res_img.copy() for res_img in walk_seq]
        for res_img in walk_right_seq:
            res_img.img = res_img.img.get_transform(flip_x=False)
        walk_left_seq = [res_img.copy() for res_img in walk_seq]
        for res_img in walk_left_seq:
            res_img.img = res_img.img.get_transform(flip_x=True)
        idle_right = stand.copy()
        idle_right.img = idle_right.img.get_transform(flip_x=False)
        idle_left = stand.copy()
        idle_left.img = idle_left.img.get_transform(flip_x=True)
        jump_right = jump.copy()
        jump_right.img = jump_right.img.get_transform(flip_x=False)
        jump_left = jump.copy()
        jump_left.img = jump_left.img.get_transform(flip_x=True)

        walk_right_anim = ResourceAnimation(res_img_path_seq=walk_right_seq, duration=1/20, loop=True)
        walk_left_anim = ResourceAnimation(res_img_path_seq=walk_left_seq, duration=1/20, loop=True)

class TileImages:
    boxAlt = ResourceImage("Tiles/boxAlt.png")
    boxCoinAlt_disabled = ResourceImage("Tiles/boxCoinAlt_disabled.png")
    boxCoinAlt = ResourceImage("Tiles/boxCoinAlt.png")
    boxCoin_disabled = ResourceImage("Tiles/boxCoin_disabled.png")
    boxCoin = ResourceImage("Tiles/boxCoin.png")
    boxEmpty = ResourceImage("Tiles/boxEmpty.png")
    boxExplosiveAlt = ResourceImage("Tiles/boxExplosiveAlt.png")
    boxExplosive_disabled = ResourceImage("Tiles/boxExplosive_disabled.png")
    boxExplosive = ResourceImage("Tiles/boxExplosive.png")
    boxItemAlt_disabled = ResourceImage("Tiles/boxItemAlt_disabled.png")
    boxItemAlt = ResourceImage("Tiles/boxItemAlt.png")
    boxItem_disabled = ResourceImage("Tiles/boxItem_disabled.png")
    boxItem = ResourceImage("Tiles/boxItem.png")
    box = ResourceImage("Tiles/box.png")
    boxWarning = ResourceImage("Tiles/boxWarning.png")
    brickWall = ResourceImage("Tiles/brickWall.png")
    bridgeLogs = ResourceImage("Tiles/bridgeLogs.png")
    bridge = ResourceImage("Tiles/bridge.png")
    castleCenter = ResourceImage("Tiles/castleCenter.png")
    castleCenter_rounded = ResourceImage("Tiles/castleCenter_rounded.png")
    castleCliffLeftAlt = ResourceImage("Tiles/castleCliffLeftAlt.png")
    castleCliffLeft = ResourceImage("Tiles/castleCliffLeft.png")
    castleCliffRightAlt = ResourceImage("Tiles/castleCliffRightAlt.png")
    castleCliffRight = ResourceImage("Tiles/castleCliffRight.png")
    castleHalfLeft = ResourceImage("Tiles/castleHalfLeft.png")
    castleHalfMid = ResourceImage("Tiles/castleHalfMid.png")
    castleHalf = ResourceImage("Tiles/castleHalf.png")
    castleHalfRight = ResourceImage("Tiles/castleHalfRight.png")
    castleHillLeft2 = ResourceImage("Tiles/castleHillLeft2.png")
    castleHillLeft = ResourceImage("Tiles/castleHillLeft.png")
    castleHillRight2 = ResourceImage("Tiles/castleHillRight2.png")
    castleHillRight = ResourceImage("Tiles/castleHillRight.png")
    castleLedgeLeft = ResourceImage("Tiles/castleLedgeLeft.png")
    castleLedgeRight = ResourceImage("Tiles/castleLedgeRight.png")
    castleLeft = ResourceImage("Tiles/castleLeft.png")
    castleMid = ResourceImage("Tiles/castleMid.png")
    castle = ResourceImage("Tiles/castle.png")
    castleRight = ResourceImage("Tiles/castleRight.png")
    dirtCenter = ResourceImage("Tiles/dirtCenter.png")
    dirtCenter_rounded = ResourceImage("Tiles/dirtCenter_rounded.png")
    dirtCliffLeftAlt = ResourceImage("Tiles/dirtCliffLeftAlt.png")
    dirtCliffLeft = ResourceImage("Tiles/dirtCliffLeft.png")
    dirtCliffRightAlt = ResourceImage("Tiles/dirtCliffRightAlt.png")
    dirtCliffRight = ResourceImage("Tiles/dirtCliffRight.png")
    dirtHalfLeft = ResourceImage("Tiles/dirtHalfLeft.png")
    dirtHalfMid = ResourceImage("Tiles/dirtHalfMid.png")
    dirtHalf = ResourceImage("Tiles/dirtHalf.png")
    dirtHalfRight = ResourceImage("Tiles/dirtHalfRight.png")
    dirtHillLeft2 = ResourceImage("Tiles/dirtHillLeft2.png")
    dirtHillLeft = ResourceImage("Tiles/dirtHillLeft.png")
    dirtHillRight2 = ResourceImage("Tiles/dirtHillRight2.png")
    dirtHillRight = ResourceImage("Tiles/dirtHillRight.png")
    dirtLedgeLeft = ResourceImage("Tiles/dirtLedgeLeft.png")
    dirtLedgeRight = ResourceImage("Tiles/dirtLedgeRight.png")
    dirtLeft = ResourceImage("Tiles/dirtLeft.png")
    dirtMid = ResourceImage("Tiles/dirtMid.png")
    dirt = ResourceImage("Tiles/dirt.png")
    dirtRight = ResourceImage("Tiles/dirtRight.png")
    door_closedMid = ResourceImage("Tiles/door_closedMid.png")
    door_closedTop = ResourceImage("Tiles/door_closedTop.png")
    door_openMid = ResourceImage("Tiles/door_openMid.png")
    door_openTop = ResourceImage("Tiles/door_openTop.png")
    fenceBroken = ResourceImage("Tiles/fenceBroken.png")
    fence = ResourceImage("Tiles/fence.png")
    grassCenter = ResourceImage("Tiles/grassCenter.png")
    grassCenter_rounded = ResourceImage("Tiles/grassCenter_rounded.png")
    grassCliffLeftAlt = ResourceImage("Tiles/grassCliffLeftAlt.png")
    grassCliffLeft = ResourceImage("Tiles/grassCliffLeft.png")
    grassCliffRightAlt = ResourceImage("Tiles/grassCliffRightAlt.png")
    grassCliffRight = ResourceImage("Tiles/grassCliffRight.png")
    grassHalfLeft = ResourceImage("Tiles/grassHalfLeft.png")
    grassHalfMid = ResourceImage("Tiles/grassHalfMid.png")
    grassHalf = ResourceImage("Tiles/grassHalf.png")
    grassHalfRight = ResourceImage("Tiles/grassHalfRight.png")
    grassHillLeft2 = ResourceImage("Tiles/grassHillLeft2.png")
    grassHillLeft = ResourceImage("Tiles/grassHillLeft.png")
    grassHillRight2 = ResourceImage("Tiles/grassHillRight2.png")
    grassHillRight = ResourceImage("Tiles/grassHillRight.png")
    grassLedgeLeft = ResourceImage("Tiles/grassLedgeLeft.png")
    grassLedgeRight = ResourceImage("Tiles/grassLedgeRight.png")
    grassLeft = ResourceImage("Tiles/grassLeft.png")
    grassMid = ResourceImage("Tiles/grassMid.png")
    grass = ResourceImage("Tiles/grass.png")
    grassRight = ResourceImage("Tiles/grassRight.png")
    hill_largeAlt = ResourceImage("Tiles/hill_largeAlt.png")
    hill_large = ResourceImage("Tiles/hill_large.png")
    hill_smallAlt = ResourceImage("Tiles/hill_smallAlt.png")
    hill_small = ResourceImage("Tiles/hill_small.png")
    ladder_mid = ResourceImage("Tiles/ladder_mid.png")
    ladder_top = ResourceImage("Tiles/ladder_top.png")
    liquidLava = ResourceImage("Tiles/liquidLava.png")
    liquidLavaTop_mid = ResourceImage("Tiles/liquidLavaTop_mid.png")
    liquidLavaTop = ResourceImage("Tiles/liquidLavaTop.png")
    liquidWater = ResourceImage("Tiles/liquidWater.png")
    liquidWaterTop_mid = ResourceImage("Tiles/liquidWaterTop_mid.png")
    liquidWaterTop = ResourceImage("Tiles/liquidWaterTop.png")
    lock_blue = ResourceImage("Tiles/lock_blue.png")
    lock_green = ResourceImage("Tiles/lock_green.png")
    lock_red = ResourceImage("Tiles/lock_red.png")
    lock_yellow = ResourceImage("Tiles/lock_yellow.png")
    rockHillLeft = ResourceImage("Tiles/rockHillLeft.png")
    rockHillRight = ResourceImage("Tiles/rockHillRight.png")
    ropeAttached = ResourceImage("Tiles/ropeAttached.png")
    ropeHorizontal = ResourceImage("Tiles/ropeHorizontal.png")
    ropeVertical = ResourceImage("Tiles/ropeVertical.png")
    sandCenter = ResourceImage("Tiles/sandCenter.png")
    sandCenter_rounded = ResourceImage("Tiles/sandCenter_rounded.png")
    sandCliffLeftAlt = ResourceImage("Tiles/sandCliffLeftAlt.png")
    sandCliffLeft = ResourceImage("Tiles/sandCliffLeft.png")
    sandCliffRightAlt = ResourceImage("Tiles/sandCliffRightAlt.png")
    sandCliffRight = ResourceImage("Tiles/sandCliffRight.png")
    sandHalfLeft = ResourceImage("Tiles/sandHalfLeft.png")
    sandHalfMid = ResourceImage("Tiles/sandHalfMid.png")
    sandHalf = ResourceImage("Tiles/sandHalf.png")
    sandHalfRight = ResourceImage("Tiles/sandHalfRight.png")
    sandHillLeft2 = ResourceImage("Tiles/sandHillLeft2.png")
    sandHillLeft = ResourceImage("Tiles/sandHillLeft.png")
    sandHillRight2 = ResourceImage("Tiles/sandHillRight2.png")
    sandHillRight = ResourceImage("Tiles/sandHillRight.png")
    sandLedgeLeft = ResourceImage("Tiles/sandLedgeLeft.png")
    sandLedgeRight = ResourceImage("Tiles/sandLedgeRight.png")
    sandLeft = ResourceImage("Tiles/sandLeft.png")
    sandMid = ResourceImage("Tiles/sandMid.png")
    sand = ResourceImage("Tiles/sand.png")
    sandRight = ResourceImage("Tiles/sandRight.png")
    signExit = ResourceImage("Tiles/signExit.png")
    signLeft = ResourceImage("Tiles/signLeft.png")
    sign = ResourceImage("Tiles/sign.png")
    signRight = ResourceImage("Tiles/signRight.png")
    snowCenter = ResourceImage("Tiles/snowCenter.png")
    snowCenter_rounded = ResourceImage("Tiles/snowCenter_rounded.png")
    snowCliffLeftAlt = ResourceImage("Tiles/snowCliffLeftAlt.png")
    snowCliffLeft = ResourceImage("Tiles/snowCliffLeft.png")
    snowCliffRightAlt = ResourceImage("Tiles/snowCliffRightAlt.png")
    snowCliffRight = ResourceImage("Tiles/snowCliffRight.png")
    snowHalfLeft = ResourceImage("Tiles/snowHalfLeft.png")
    snowHalfMid = ResourceImage("Tiles/snowHalfMid.png")
    snowHalf = ResourceImage("Tiles/snowHalf.png")
    snowHalfRight = ResourceImage("Tiles/snowHalfRight.png")
    snowHillLeft2 = ResourceImage("Tiles/snowHillLeft2.png")
    snowHillLeft = ResourceImage("Tiles/snowHillLeft.png")
    snowHillRight2 = ResourceImage("Tiles/snowHillRight2.png")
    snowHillRight = ResourceImage("Tiles/snowHillRight.png")
    snowLedgeLeft = ResourceImage("Tiles/snowLedgeLeft.png")
    snowLedgeRight = ResourceImage("Tiles/snowLedgeRight.png")
    snowLeft = ResourceImage("Tiles/snowLeft.png")
    snowMid = ResourceImage("Tiles/snowMid.png")
    snow = ResourceImage("Tiles/snow.png")
    snowRight = ResourceImage("Tiles/snowRight.png")
    stoneCenter = ResourceImage("Tiles/stoneCenter.png")
    stoneCenter_rounded = ResourceImage("Tiles/stoneCenter_rounded.png")
    stoneCliffLeftAlt = ResourceImage("Tiles/stoneCliffLeftAlt.png")
    stoneCliffLeft = ResourceImage("Tiles/stoneCliffLeft.png")
    stoneCliffRightAlt = ResourceImage("Tiles/stoneCliffRightAlt.png")
    stoneCliffRight = ResourceImage("Tiles/stoneCliffRight.png")
    stoneHalfLeft = ResourceImage("Tiles/stoneHalfLeft.png")
    stoneHalfMid = ResourceImage("Tiles/stoneHalfMid.png")
    stoneHalf = ResourceImage("Tiles/stoneHalf.png")
    stoneHalfRight = ResourceImage("Tiles/stoneHalfRight.png")
    stoneHillLeft2 = ResourceImage("Tiles/stoneHillLeft2.png")
    stoneHillRight2 = ResourceImage("Tiles/stoneHillRight2.png")
    stoneLedgeLeft = ResourceImage("Tiles/stoneLedgeLeft.png")
    stoneLedgeRight = ResourceImage("Tiles/stoneLedgeRight.png")
    stoneLeft = ResourceImage("Tiles/stoneLeft.png")
    stoneMid = ResourceImage("Tiles/stoneMid.png")
    stone = ResourceImage("Tiles/stone.png")
    stoneRight = ResourceImage("Tiles/stoneRight.png")
    stoneWall = ResourceImage("Tiles/stoneWall.png")
    tiles_spritesheet = ResourceImage("Tiles/tiles_spritesheet.png")
    tochLit2 = ResourceImage("Tiles/tochLit2.png")
    tochLit = ResourceImage("Tiles/tochLit.png")
    torch = ResourceImage("Tiles/torch.png")
    window = ResourceImage("Tiles/window.png")
