import arcade
import os
import random

INSTRUCTION_PAGE = 1
GAME_RUNNING = 2
GAME_OVER = 3
SPRITE_SCALING_PLAYER = 0.4
SPRITE_SCALING_CLOUD = 0.9
SPRITE_SCALING_COIN = 0.8
SPRITE_SCALING_BAD_COIN = 0.6
SCREEN_WIDTH = 880
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 5
VIEWPORT_MARGIN = 40
GRAVITY = 0.5
JUMP_SPEED = 6.5


class MyWindow(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        self.all_sprites_list = None
        self.player_sprite_list = None
        self.wall_list = None
        self.coin_list = None
        self.bad_coin_list = None
        self.player_sprite = None
        self.coin = 0
        self.bad_coin = 0
        

        self.view_bottom = 0
        self.view_left = 0
        self.physics_engine = None 

        arcade.set_background_color(arcade.color.CAMEO_PINK)

        self.current_state = GAME_RUNNING
        
        self.total_time = 0.0

 

    def setup(self):

        self.cameraspeed= 1
        self.coincounter=20
        self.coincounter2=30
        self.timerpos=300
        self.over_x= 240
        self.over_y= 200
        
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bad_coin_list = arcade.SpriteList()

        self.all_sprites_list = arcade.SpriteList()
        self.player_sprite_list = arcade.SpriteList()
        self.total_time = 0.0

        #wall
        for y in range(-10000,500, 130):
            for x in range(35, 880,75):
                if random.randrange(9) > 4.5:
                    wall = arcade.Sprite("cloud.png", SPRITE_SCALING_CLOUD)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
        wall = arcade.Sprite("cloud.png", SPRITE_SCALING_CLOUD)
        wall.center_x = 35
        wall.center_y = 420
        self.wall_list.append(wall)

        #coin
        for z in range(-9970,470, 130):
            for p in range(35, 880, 64):
                if random.randrange(9) > 6:
                    coin = arcade.Sprite("coin.png", SPRITE_SCALING_COIN)
                    coin.center_x = p
                    coin.center_y = z
                    self.coin_list.append(coin)

        #bad Coin 
        for y in range(-9970,470, 130):
            for x in range(30, 700, 60):
                if random.randrange(9) > 7.5:
                    bad_coin = arcade.Sprite("candy.png", SPRITE_SCALING_BAD_COIN)
                    bad_coin.center_x = x
                    bad_coin.center_y = y
                    self.bad_coin_list.append(bad_coin)
           

        #pegacorn
        self.player_sprite = arcade.Sprite("pegacornn.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 35
        self.player_sprite.center_y = 500
        self.player_sprite_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                     self.wall_list,
                                                     gravity_constant=GRAVITY)

    def draw_game_over(self):
 
        arcade.draw_text("Game Over", self.over_x, self.over_y, arcade.color.WHITE, 54)
        
    def draw_game(self):
        self.player_sprite_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.bad_coin_list.draw()
        output = f"$:{self.coin}"
        arcade.draw_text(output,40,self.coincounter,arcade.color.GOLD,15)
        output = f"Bad Candy:{self.bad_coin}"
        arcade.draw_text(output,40,self.coincounter2,arcade.color.ALLOY_ORANGE,15)
        arcade.draw_text("Collect 120 coins to win! Be Careful though if you eat 20 pieces of candy the pegacorn will have a toothache :) ", 20, 70, arcade.color.COPPER_ROSE, 14)
    def on_draw(self):
        arcade.start_render()
        if self.current_state == GAME_RUNNING:
            minutes = int(self.total_time) // 60
            seconds = int(self.total_time) % 60
            output = f"Time: {minutes:02d}:{seconds:02d}"
            arcade.draw_text(output, 300, self.timerpos, arcade.color.WHITE, 30)
            self.draw_game()
        else:
            self.draw_game()
            self.draw_game_over()
            

            
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        if self.current_state == GAME_RUNNING:
            if self.player_sprite.right>880:
                self.player_sprite.right=880
            if self.player_sprite.left<0:
                self.player_sprite.left=0
            
            self.total_time += delta_time
            #self.player_sprite.update()
            self.physics_engine.update()
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                            self.coin_list)
            bad_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.bad_coin_list)
            for coin in hit_list:
                coin.kill()
                self.coin += 1
            for badCoin in bad_list:
                badCoin.kill()
                self.bad_coin += 1
                
            #self.wall_list.update()
            changed = False

            # Scroll down
            bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
            if self.player_sprite.center_y < self.view_bottom:
                self.view_bottom -= self.cameraspeed*6
                self.coincounter = self.view_bottom +5
                self.coincounter2 = self.view_bottom +20
                self.timerpos = self.view_bottom + 10
                self.over_y = self.view_bottom + 450

            else:
                self.view_bottom -= self.cameraspeed
                self.coincounter=self.view_bottom + 5
                self.coincounter2 = self.view_bottom +20
                self.timerpos = self.view_bottom + 10
                self.over_y = self.view_bottom + 450
              
            #if self.player_sprite
            changed = True

            # Make sure our boundaries are integer values.
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)

            # If we changed the boundary values, update the view port to match
            if changed:
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left - 1,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom - 1)
            if self.bad_coin == 2:
                self.current_state = GAME_OVER
            if self.coin == 120:
                self.current_state = GAME_OVER

def main():
    
    window = MyWindow()
    window.setup()
    arcade.run()
    main()
    


main()
