# Primitive engine 

Welcome to Primitive engine documentation!

Primitive engine is based on pygame_tools_tafh module, and is written on python as a wrapper for pygame module.

---

# Example

It is example of red circle object on the screen

```py
from engine_antiantilopa import *

# Create Engine with 700x500 window
e = Engine(Vector2d(700, 500))


# Bind keys for movement of camera (Default wasd)
bind_keys_for_camera_movement()

# Create Game object with Coords <0, 0> and surface 500x500
world = GameObject("world")
world.add_component(Transform(Vector2d(0, 0)))
world.add_component(SurfaceComponent(Vector2d(500, 500)))

# bind world to the root of gameobjects chain
GameObject.root.add_child(world)

# Create Game object with Coords <0, 0>, red color, and surface 500x500
button = GameObject("button")

button.add_component(CircleShapeComponent(100))
button.add_component(Transform(Vector2d(0, 0)))
button.add_component(ColorComponent((255, 0, 0)))
button.add_component(SurfaceComponent(Vector2d(500, 500)))

# bind button to world object
world.add_child(button)

#run engine
e.run()

```

---

# Relative links:
- [Engine](#engine)
- [Game Object](#game-object)
- [Component](#component)
- [Surface Component](#surface-component)
- [Color Component](#color-component)
- [Shape Component](#shape-component)
- [Circle Shape Component](#circle-shape-component)
- [Rect Shape Component](#rect-shape-component)
- [On Click Component](#on-click-component)
- [Key Bind Component](#key-bind-component)
- [Label Component](#label-component)
- [Sprite Component](#sprite-component)
- [Entry Component](#entry-component)
- [Camera](#camera)
- [Vector Math](#vector-math)
- - [Vector2d](#vector2d)
- - [Angle](#angle)
---

# Engine

main object of programm
> Engine() -> Engine
> Engine(window_size: Vector2d) -> Engine

- [draw()](#enginedraw)
- [first_iteration()](#enginefirst_iteration)
- [iteration()](#engineiteration)
- [run()](#enginerun)
- [update()](#engineupdate)
- [set_debug()](#engineset_debug)
- [forced_blit()](#engineforced_blit)
<br>
The *Engine* class gathers and launches all code at once. Default init creates window size equal to size of display.

**Arguments:**
- window_size (Vector2d | tuple[int, int]) <br> size of created window.

**Returns:**
- newly created *Engine* object.

**Variables:**
- no parameters

### Engine.first_iteration()
Engine.first_iteration() -> None
Calls [first_iteration()](#gameobjectfirst_iteration) method from all [game objects](#game-object).

### Engine.iteration()
Engine.iteration() -> None
Calls [iteration()](#gameobjectiteration) method from all [game objects](#game-object).

### Engine.draw()
Engine.draw() -> None
First, all surfaces that need to be cleared are cleared. The need is defined as whether one of oncomers need_blit is equal true, and it is in camera view, or game object need_draw is true. Then, calls [draw()](#gameobjectdraw) method from all game objects. After, it blits all surfaces, whose need_blit is True and is in camera view, according to oncoming preference. The way it works is that: child object is always higher than its parent. game objects that are not in camera view does not blit, so need_blit does not change.

### Engine.refresh()
Engine.update() -> None
Calls [refresh()](#compomemtrefresh) method from all component classes.

### Engine.run()
Engine.run(fps: float) -> None
runs pygame application with given frame rate in a loop until window quit or error occur. Before main loop, *first_iteration()* method is called. In the loop, the methods are called in the given order:
1. iteration()
2. draw()
3. refresh()
4. pygame.display.flip()

### Engine.set_debug()
Engine.set_debug(value: bool) -> None
Static method. Sets global DEBUG variable equal to value.

### Engine.forced_blit()
Engine.draw() -> None
calls iteration(), calls [draw()](#gameobjectdraw) from all game objects, then blits all surfaces, according to oncoming preference (as in draw()).

---

# Game Object

object for all game "objects"
> GameObject() -> GameObject
> GameObject(tags: str) -> GameObject
> GameObject(tags: list\[str]) -> GameObject

- [get_group_by_tag()](#gameobjectget_group_by_tag)
- [get_game_object_by_tags()](#gameobjectget_game_object_by_tags)
- [add_component()](#gameobjectadd_component)
- [add_child()](#gameobjectadd_child)
- [get_component()](#gameobjectget_component)
- [contains_component()](#gameobjectcontains_component)
- [get_childs()](#gameobjectget_childs)
- [first_iteration()](#gameobjectfirst_iteration)
- [iteration()](#gameobjectiteration)
- [draw()](#gameobjectdraw)
- [enable()](#gameobjectenable)
- [disable()](#gameobjectdisable)
- [destroy()](#gameobjectdestroy)
- [show_geneology_tree()](#gameobjectshow_geneology_tree)
- [need_draw_set_true()](#gameobjectneed_draw_set_true)
- [need_blit_set_true()](#gameobjectneed_blit_set_true)
<br>

The *GameObject* class is a kind of container for [components](#component). It can be accessed by its tags. Default init creates empty GameObject without tags. For Gameobjects, [Transform](#transform) and [Surface](#surface-component) Components are necessary.

**Arguments:**
- tags (list\[str] | str) <br> tag or list of tags to identify game object 

**Returns:**
- newly created *GameObject* object.

**Variables:**
- tags (list\[str]) <br> all tags of the game objects.
- components (list[[Component](#component)]) <br> all components of the game object.
- childs (list[[GameObject](#game-object)]) <br> all game objects binded to the game object.
- parent ([GameObject](#game-object)) <br> a game object that the game object is binded to.
- active (bool) <br> state of the game object. If not active, it will not iterate or be drawn on screen.
- need_draw (bool) <br> flag variable. if true, game object will be drawn.
- need_blit (bool) <br> flag variable. if true and game object is on screen (absolute cordinates touches screen), game object will be blit.
- need_first_iteration (bool) <br> flag variable. if true, game object will call *first_iteration* instead of *iteration*.

**Static Variables:**
- root ([GameObject](#game-object)) <br> root game object representing screen. all gameobject have to be chained to it to be drawn. 
- objs (list\[[GameObject](#game-object)]) <br> all initialized game objects list. Initially empty
- group_tag_dict (dict\[str, [GameObject](#game-object)]) <br> dictionary of tags to game objects. Initially empty.

### GameObject.get_group_by_tag()
GameObject.get_group_by_tag(tag: str) -> list\[[GameObject](#game-object)]
Static method. returns all game objects with given tag. if there are no, empty list returned.

### GameObject.get_game_object_by_tags()
GameObject.get_game_object_by_tags(*tags: list\[str]) -> [GameObject](#game-object)
Static method. returns one game object that has the given tags only. if there are more than 1 or, there are no such, Exception raised.

### GameObject.show_geneology_tree()
show_geneology_tree(game_object: [GameObject](#game-object)|None = None, depth: int = 1) -> None
prints geneology tree starting from given game object. Default starting point is root game object.

### GameObject.add_component()
GameObject.add_component(component: [Component](#component)) -> None
adds given component to components list of the game object

### GameObject.add_child()
GameObject.add_child(child: [GameObject](#game-object)) -> None
binds given game object to the game object

### GameObject.get_component()
GameObject.get_component(component_type: type\[T]) -> T
returns component of a given type. If there is no such, Key error exception is raised

### GameObject.contains_component()
GameObject.contains_component(component_type: type\[T]) -> bool
checks if the game object has component of given type.

### GameObject.get_childs()
GameObject.get_childs(tag: str) -> list\[[GameObject](#game-object)]
returns all childs of the components with a given tag.

### GameObject.first_iteration()
GameObject.first_iteration() -> None
Calls [first_iteration()](#componentfirst_iteration) method for all components of the game object.

### GameObject.iteration()
GameObject.iteration() -> None
Calls [iteration()](#componentiteration) method for all components of the game object.

### GameObject.draw()
GameObject.draw() -> None
if need_draw and acive are both True, calls [draw()](#componentdraw) method for all components of the game object.

### GameObject.enable()
GameObject.enable() -> None
sets acrive variable equal to True and enables all game objects chained to this game object.

### GameObject.disable()
GameObject.disable() -> None
sets acrive variable equal to False and disables all game objects chained to this game object.

### GameObject.need_draw_set_true()
GameObject.need_draw_set_true() -> None
Sets need_draw equal to true, and if parent exists, calls *need_draw_set_true()* method for parent.

### GameObject.need_blit_set_true()
GameObject.need_blit_set_true() -> None
Sets need_blit equal to true, and if parent exists, calls *need_blit_set_true()* method for parent.

> [!WARNING]
> changing *need_draw* or *need_blit* manually, can cause unexpected errors.

### GameObject.destroy()
GameObject.destroy() -> None
destroys game object and all childs and components of the game object. Removes it from tag dictionary, objs list, and parents' childs list. need blit sets true to update.

---

# Component
base class for other components in game. Not used directly.
> Component() -> Component

- [fisrt_iteration()](#componentfirst_iteration)
- [iteration()](#componentiteration)
- [draw()](#componentdraw)
- [refresh()](#componentrefresh)
- [destroy()](#componentdestroy)
<br>

**Arguments:**
- no arguments

**Returns:**
- no returns

**Variables:**
- game_object ([GameObject](#game-object)) <br> game_object that contains the component

**Static Variables:**
- component_classes (list\[type\[Component]]) <br> list of all classes that inherited from Component

### Component.first_iteration()
Component.first_iteration() -> None
does nothing

### Component.iteration()
Component.iteration() -> None
does nothing

### Component.draw()
Component.draw() -> None
does nothing

### Component.refresh()
Component.refresh() -> None
Static method. does nothing

### Component.destroy()
Component.destroy() -> None
does nothing

---

# Transform
Child class of [Component](#component).
object for representing position and rotation in 2 dimensions.
> Transform() -> Transform
> Transform(pos: Vector2d) -> Transform
> Transform(rotation: Angle|float) -> Transform
> Transform(pos: Vector2d, rotation: Angle|float) -> Transform

- [first_iteration](#transformfirst_iteration)
- [move()](#transformmove)
- [rotate()](#transformrotate)
- [set_pos()](#transformset_pos)
- [set_rotation()](#transformset_rotation)
- [update_abs_pos()](#transformupdate_abs_pos)
- [refresh()](#transformrefresh)
<br>

**Arguments:**
- pos (Vector2d) <br> position of the **center** of the game object.
- rotation (Angle | float) <br> angle of the gameobject. ***Not working now!!!***

**Returns:**
- newly created *Transform* object.

**Variables:**
- pos (Vector2d) <br> position of the **center** of the game object relative to its parent's **center**.
- abs_pos (Vector2d) <br> position of **center** of the game object relative to main screen's **center**.
- rotation (Angle) <br> angle of the gameobject.
- changed (bool) <br> flag variable. Shows whether Trnasform has changed. Initially False

**Static Variables:**
- objs (list\[Transform]) <br> list of all Transform instances.

### Transform.first_iteration()
Transform.first_iteration() -> None
Finds abs_pos for all Transform instances.

### Transform.move()
Transform.move(delta: Vector2d) -> None
Changes *pos* with given delta, sets *changed* equal to True. Calls [need_blit_set_true()](#gameobjectneed_blit_set_true) for the game object. Calls *update_abs_pos()* for self.

### Transform.rotate()
Transform.rotate(delta: Angle) -> None
Changes *rotation* with given delta. **Not working now !!!**

### Transform.set_pos()
Transform.set_pos(pos: Vector2d) -> None
Sets *pos* equal to pos, sets *changed* equal to True. Calls [need_blit_set_true()](#gameobjectneed_blit_set_true) for the game object. Calls *update_abs_pos()* for self.


### Transform.set_rotation()
Transform.set_rotation(rotation: Angle) -> None
Sets *rotation* equal to given rotation. **Not working now !!!**

### Transform.update_abs_pos()
Transform.update_abs_pos(abs_pos: Vector2d) -> None
Sets *abs_pos* equal to given abs_pos + *pos*. Calls update_abs_pos(*abs_pos*) from all childs of the game object.

### Transform.refresh()
Transform.refresh() -> None
Static method. Sets *changed* equal to False for all instances of Transform.

---

# Surface Component
Child class of [Component](#component).
object for representing surface where everything is drawn.
> SurfaceComponent(size: Vector2d, crop: bool = True) -> SurfaceComponent

- [first_iteration()](#surfacecomponentfirst_iteration)
- [blit()](#surfacecomponentblit)
- [update_oncoming()](#surfacecomponentupdate_oncoming)
- [add_oncoming()](#surfacecomponentadd_oncoming)
- [remove_oncoming()](#surfacecomponentremove_oncoming)
- [destroy()](#surfacecomponentdestroy)
<br>

**Requirements:**
- [Transform Component](#transform)
- parent with Surface Component

**Arguments:**
- size (Vector2d) <br> size of surface and game object.
- crop (bool) <br> flag variable. shows whether or not the surface should be cropped by parent surface. Initially True.
- layer (int) <br> the layer of the surface. Initially 1

> [!WARNING]
> layer variable should not be negative. if layer is negative, some functions may not work!

**Returns:**
- newly created *SurfaceComponent* object.

**Variables:**
- size: Vector2d <br> size of surface and game object.
- pg_surf: pygame.Surface <br> actual pygame surface where child game objects will be drawn
- crop (bool) <br> flag: whether or not the surface should be cropped by parent surface. When True, it is much easier for computer to run the game
- depth (int) <br> shows to which depth it needs to "fall". equal 1 if *crop*.
- oncoming (list\[[GameObject](#game-object)]) <br> list of game objects that will be blit on the surface
- layer (int) <br> the layer of the surface. higher the layer variable, higher the surface will be. 

> [!NOTE]
> the layer do not affect game objects that has different parent. If two objects with the same parent have the same layer variable, the overlay will be hardly determined! 

### SurfaceComponent.first_iteration()
SurfaceComponent.first_iteration() -> None
Tries to find where each surface should be blit. If *crop*, then it will blit on parent even if it is not fully inside it.

### SurfaceComponent.blit()
SurfaceComponent.blit() -> None
Blits the surface to parent surface. If game object is root, nothing happens. (because root has not parent game object). If someone under the surface changed its position ([Transform.changed](#transform)), calls *update_oncoming()*

### SurfaceComponent.update_oncoming()
SurfaceComponent.update_oncoming() -> tuple\[Vector2d, SurfaceComponent]
Updates *depth* of the Surface component, so that it will blit without crops. Returns position relative to the game object that surface will blit on, and its Surface component.

### SurfaceComponent.add_oncoming()
SurfaceComponent.add_oncoming(g_obj: [GameObject](#game-object)) -> None
Inserts given game object in *oncoming* so that list is sorted according to their Surface component's depth and layer variables.

> [!NOTE]
> the rich compare function for insort of game objects is: 
> \[depth - \frac{1}{1 + layer}\] 
> it can be seen that if layer is negative, then the fraction will be more than 1, thus it will overshadow depth difference. though, nothing stops layer from being a fraction > 0.

### SurfaceComponent.remove_oncoming()
SurfaceComponent.remove_oncoming(g_obj: [GameObject](#game-object)) -> None
Removes given game object from *oncoming* if it was there.

### SurfaceComponent.destroy()
SurfaceComponent.destroy() -> None
calls remove_oncoming(self) for game object's Surface component to which the surface would have been blit on.


---

# Color Component
child class of [Component](#component).
object for representation of color in RGB.

> ColorComponent(color: tuple\[int, int, int]) -> ColorComponent

**Arguments:**
- color (tuple\[int, int, int]) <br> RGB color of game object. each number must be in range (0, 256).

**Returns:**
- newly created *ColorComponent* object.

**Variables:**
- color (tuple\[int, int, int]) <br> RGB color of game object. each number must be in range (0, 256).

**Static Variables:**
- FUCKING_BLACKEST_NIGGER = (-2\*\*32 + 1, -2\*\*32 + 1, -2\*\*32 + 1)

- BLACK = (0, 0, 0)
- WHITE = (255, 255, 255)
- RED = (255, 0, 0)
- GREEN = (0, 255, 0)
- BLUE = (0, 0, 255)
- YELLOW = (255, 255, 0)
- PURPLE = (255, 0, 255)
- CYAN = (0, 255, 255)

---

# Shape Component
Child class of [Component](#component).
base object for representing various shapes. 
> ShapeComponent(collide_formula: Callable\[\[Vector2d], bool]) -> ShapeComponent

- [does_collide()](#shapecomponentdoes_collide)
<br>

**Requirements:**
- [Transform Component](#transform)

**Arguments:**
- collide_formula (Callable\[\[Vector2d], bool]) <br> formula which will return whether given Vector2d lies in a shape if its center is at \<0, 0\>.

**Returns:**
- newly created *ShapeComponent* object.

### ShapeComponent.does_collide()
ShapeComponent.does_collide(pos: Vector2d) -> bool
check if given Vector2d lies in a shape centered in transform.

---

# Circle Shape Component
Child class of [ShapeComponent](#shape-component).
represent circle shape.
> CircleShapeComponent(radius: float) -> CircleShapeComponent
> CircleShapeComponent(radius: float, need_draw: bool) -> CircleShapeComponent

- [does_collide()](#circleshapecomponentdoes_collide)
- [draw()](#circleshapecomponentdraw)
<br>

**Requirements:**
- [Transform Component](#transform)
- [Surface Component](#surface-component) (if contains [Color Component](#color-component))

**Arguments:**
- radius (float) <br> radius of issued circle shape
- need_draw (bool) <br> will the circle be drawn or not. Initially True

**Returns:**
- newly created *CircleShapeComponent* object.

**Variables:**
- radius (float) <br> radius of issued circle shape
- need_draw (bool) <br> will the circle be drawn or not.

### CircleShapeComponent.does_collide()
CircleShapeComponent.does_collide(pos: Vector2d) -> bool
check if given pos lies in circle centered in transform, with known radius.

### CircleShapeComponent.draw()
CircleShapeComponent.draw() -> None
if need_draw is True and game object contains [Color Component](#color-component), draws circle centered in transform, with known radius and color.

---

# Rect Shape Component
Child class of [ShapeComponent](#shape-component).
represent rectangle shape.
> RectShapeComponent(size: Vector2d) -> RectShapeComponent
> RectShapeComponent(size: Vector2d, need_draw: bool) -> RectShapeComponent

- [does_collide()](#rectshapecomponentdoes_collide)
- [draw()](#rectshapecomponentdraw)
<br>

**Requirements:**
- [Transform Component](#transform)
- [Surface Component](#surface-component) (if contains [Color Component](#color-component))

**Arguments:**
- size (Vector2d) <br> width and height of issued rectangle shape
- need_draw (bool) <br> will the rectangle be drawn or not. Initially True

**Returns:**
- newly created *RectShapeComponent* object

**Variables:**
- size (Vector2d) <br> width and height of issued rectangle shape
- need_draw (bool) <br> will the rectangle be drawn or not.

### RectShapeComponent.does_collide()
RectShapeComponent.does_collide(pos: Vector2d) -> bool
check if given pos lies in rectangle centered in transform, with known width and height.

### RectShapeComponent.draw()
RectShapeComponent.draw() -> None
if need_draw is True and game object contains [Color Component](#color-component), draws rectangle centered in transform, with known width, height, and color.

---

# On Click Component
Child class of [Component](#component).
object for listening for mouse clicks and responding to them.
> OnClickComponent(listen: tuple\[bool, bool, bool], listen_for_hold: bool, on_press: bool, cmd: Callable\[\[[GameObject](#game-object), tuple\[bool, bool, bool], Vector2d,  list\[Any]], None], *args: list\[Any], active: bool = False) -> OnClickComponent

- [iteration()](#onclickcomponentiteration)
- [get_relative_coord()](#onclickcomponentget_relative_coord)
<br>

**Requirements:**
- [Transform](#transform)
- [ShapeComponent](#shape-component)

**Arguments:**
- listen (tuple\[bool, bool, bool]) <br> tuple with 3 booleans each representing whether or not should it be listened for left, center, or right mouse buttons respectively.
- listen_for_holds (bool) <br> boolean representing should it be triggered by mouse buttons changes (False) or it being held (True).
- on_press (bool) <br> boolean representing should it be triggered by mouse button release (False) or mouse button push (True). Does not affect if listen_for_holds is True
- cmd (Callable\[\[[GameObject](#game-object), tuple\[bool, bool, bool], Vector2d,  list\[Any]], None]) <br> callable function which will be called when mouse button pressed and all requirements satisfied. First argument - game object whose OnliclkComponent was triggered; Second argument - tuple\[bool, bool, bool] which mouse button (left, center or right) triggered OnliclkComponent; Third argument - Vector2d position of mouse relative to the center of the game object 
- *args (list\[Any]) <br> arguments that will be given to cmd function. Initially empty
- active (bool) <br> flag. if false, iteration will not run

**Returns:**
- newly created *OnClickComponent* object.

**Variables:**
- listen (tuple\[bool, bool, bool]) <br> tuple of 3 booleans each representing whether or not should it be listened for left, center, or right mouse buttons respectively.
- listen_for_holds (bool) <br> boolean representing should it be triggered by mouse buttons changes (False) or it being held (True).
- on_press (bool) <br> boolean representing should it be triggered by mouse button release (False) or mouse button push (True). Does not affect if listen_for_holds is True
- cmd (Callable\[\[[GameObject](#game-object), tuple\[bool, bool, bool]], None]) <br> callable function which will be called when mouse button pressed and all requirements satisfied. First argument - game object whose OnliclkComponent was triggered; Second argument - tuple\[bool, bool, bool] which mouse button (left, center or right) triggered OnliclkComponent.
- previous (tuple\[bool, bool, bool]) <br> tuple of 3 booleans each representing mouse buttons state at previous iteration. *It is not updated if listen_for_holds is False*.
- args (list\[Any]) <br> arguments that will be given to cmd function.
- active (bool) <br> flag. if false, iteration will not run

### OnClickComponent.iteration()
OnClickComponent.iteration() -> None
Checks active to be true. Then, if triggered and mouse position lies in game object's shape, calls *cmd(game_object, mouse_buttons, \*args)* where *game_object* is game object that contains the on click component, *mouse_buttons* are buttons that **triggered** command (not all pressed buttons), and *\*args* are arguments provided through initialization of the component.

### OnClickComponent.get_relative_coord()
OnClickComponent.get_relative_coord(pos: Vector2d) -> Vector2d
gets absolute position on actual screen/display and returns position relative to the game object's center

---

# Key Bind Component
Child class of [Component](#component).
object for listening for keyboard clicks and responding to them.
> KeyBindComponent(listen: tuple\[int], listen_for_hold: bool, on_press: bool,  cmd: Callable\[\[[GameObject](#game-object), tuple\[int], list\[Any]], None], *args: list\[Any], active: bool = True) -> KeyBindComponent

- [iteration()](#keybindcomponentiteration)
<br>

**Arguments:**
- listen (tuple\[int]) <br> tuple of integers each representing whether or not should it be listened for keyboard keys according to pygame keys indexation.
- listen_for_holds (bool) <br> boolean representing should it be triggered by keyboard keys changes (False) or they being held (True).
- on_press (bool) <br> boolean representing should it be triggered by keyboard keys releases (False) or their pushes (True). Does not affect if listen_for_holds is True
- cmd (Callable\[\[[GameObject](#game-object), tuple\[int], list\[Any]], None]) <br> callable function which will be called when keyboard keys pressed and all requirements satisfied. First argument - game object whose KeyBindComponent was triggered; Second argument - tuple\[int] which keyboard keys (according to pygame keys indexation) triggered KeyBindComponent.
- *args (list\[Any]) <br> arguments that will be given to cmd function. Initially empty
- active (bool) <br> flag. if false, iteration will not run

**Returns:**
- newly created *KeyBindComponent* object.

**Variables:**
- listen (tuple\[int]) <br> tuple of integers each representing whether or not should it be listened for keyboard keys according to pygame keys indexation.
- listen_for_holds (bool) <br> boolean representing should it be triggered by keyboard keys changes (False) or they being held (True).
- on_press (bool) <br> boolean representing should it be triggered by keyboard keys releases (False) or their pushes (True). Does not affect if listen_for_holds is True
- cmd (Callable\[\[[GameObject](#game-object), tuple\[int]], None]) <br> callable function which will be called when keyboard keys pressed and all requirements satisfied. First argument - game object whose KeyBindComponent was triggered; Second argument - tuple\[int] which keyboard keys (according to pygame keys indexation) triggered KeyBindComponent.
- previous (list\[int]) <br> tuple of integers each representing keyboard keys states at previous iteration. *It is not updated if listen_for_holds is False*.
- args (list\[Any]) <br> arguments that will be given to cmd function.
- active (bool) <br> flag. if false, iteration will not run

### KeyBindComponent.iteration()
KeyBindComponent.iteration() -> None
Checks active to be true. Then, check if triggered, and if it is, calls *cmd(game_object, keyboard_keys, \*args)* where *game_object* is game object that contains the key bind component, *keyboard_keys* are keys that **triggered** command (not all pressed keys), and *\*args* are arguments provided through initialization of the component.

---

# Label Component
Child class of [Component](#component).
object for text render.
> LabelComponent(text: str) -> LabelComponent
> LabelComponent(text: str, font: pygame.font.Font) -> LabelComponent

- [draw()](#labelcomponentdraw)
- [set_sys_font()](#labelcomponentset_sys_font)
<br>

**Requirements:**
- [Transform Component](#transform)
- [Color Component](#color-component)
- [Surface Component](#surface-component)

**Arguments:**
- text (str) <br> string that will be drawn. cannot have any esc commands. does not support \\n (next line).
- font (pygame.font.Font) <br> font that will be used to draw text. Initially is "Consolas" font.

**Returns:**
- newly created *LabelComponent* object.

**Variables:**
- text (str) <br> string that will be drawn. cannot have any esc commands. does not support \\n (next line).
- font (pygame.font.Font) <br> font that will be used to draw text. Initially is "Consolas", px =30 font. 

### LabelComponent.draw()
LabelComponent.draw() -> None
blits text on the surface.

### LabelComponent.set_sys_font()
LabelComponent.set_sys_font(name: str, size: int, bold = 0, italic = 0) -> None
Sets font to *pygame.font.SysFont(name, size, bold, italic)*

---

# Sprite Component
Child class of [Component](#component).
object for textures' render.
> SpriteComponent(path: str, size: Vector2d, nickname: str)

- [draw()](#spritecomponentdraw)
- [get_by_nickname()](#spritecomponentget_by_nickname)
- [is_downloaded()](#spritecomponentis_downloaded)
<br>

**Requirements:**
- [Surface Component](#surface-component)

**Arguments:**
- path (str) <br> relative or full path of needed texture. if not found, pygame error will rise up. 
- size (Vector2d) <br> **needed** size of the sprite. if the texture has different size than given it (sprite, not texture) will be reshaped.
- nickname (str) <br> the name to call downloaded texture. 

**Returns:**
- newly created *SpriteComponent* object.

**Variables:**
- path (str) <br> relative or full path of needed texture.
- size (Vector2d) <br> the size of the sprite.

**Static Variables:**
- downloaded (dict\[str, pygame.Surface]) <br> to prevent the load of the same texture multiple times, the downloaded textures are stored in static veriable.

### SpriteComponent.draw()
SpriteComponent.draw() -> None
Draws the sprite at the center of the *SurfaceComponent*'s surface

### SpriteComponent.get_by_nickname()
Spritecomponent.get_by_nickname(nickname: str) -> pygame.Surface:
Static method. returns Surface of sprite by the nickname.

### SpriteComponent.is_downloaded()
SpriteComponent.is_downloaded(nickname: str = None, path: str = None) -> bool
Static method. returns whether tecture given by either nickname or path is downloaded.

> [!NOTE]
> Either nickname or path should be given. not both, not none. 

---

# Camera
a [GameObject](#game-object) object representing camera.

**Tags:**
- "Camera"

**Components:**
- [Transform](#transform) <br> at <0, 0> with rotation = 0
- [SurfaceComponent](#surface-component) <br> with size <500, 500>

#### bind_keys_for_camera_movement()
bind_keys_for_camera_movement(keys: tuple[int, int, int, int] = (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d), speed: float = 10) -> None
function ***(not a method!)*** that binds 4 keyboard keys on camera's movement with given speed for up, left, down, right respectively. 

> [!NOTE]  
> When camera goes in one dirrection, on screen, game objects, that are not binded to camera, will look like moving opposite way.

---

# Entry Component
Child class of [Label Component](#label-component).
enables interaction with text input.
> EntryComponent(default_text: str = "", font: pygame.font.Font = None, active: bool = False)

- [iteration](#entrycomponentiteration)
- [clear](#entrycomponentclear)
<br>

**Requirements:**
- [ColorComponent](#color-component)
- [SurfaceComponent](#surface-component)

**Arguments:**
- default_text (str) <br> the text that will be shown from the start. Initially empty string ("")
- font (pygame.font.Font) <br> the font that will be used to render the text. Initially consolas with height 20 px
- active (bool) <br> flag. shows whether or not the keyboard input is captured. Initially false.

**Returns:**
- newly created *EntryComponent* object.

**Variables:**
- text (str) <br> the text that is shown.
- font (pygame.font.Font) <br> the font that will be used to render the text.
- active (bool) <br> flag. shows whether or not the keyboard input is captured.

### EntryComponent.iteration()
EntryComponent.iteration() -> None
Uses pygame events to get text input, and stores it in *text* variable. Captures *KeyDown* events to catch backspaces. 
> [!Note]
> Backspace deletes only one character, no matter how long is held!

### EntryComponent.clear()
EntryComponent.clear() -> None
Sets text equal to empty string, *need_draw* to true, and calls [*need_blit_set_true()*](#gameobjectneed_blit_set_true) method

---

# Vector math
Vector math is a module used for 2d calculations. Primitive engine uses vector math mini with only Vector2d and Angle.

# Vector2d
Class to represent a pair of floats.

> Vector2d() -> Vector2d
> Vector2d(x: float, y: float) -> Vector2d
> Vector2d.from_tuple(tpl: tuple\[float, float]) -> Vector2d

- [from_tuple()](#Vector2dfrom_tuple)
- [as_tuple()](#Vector2das_tuple)
- [distance()](#Vector2ddistance)
- [length()](#vector2dlength)
- [norm()](#Vector2dnorm)
- [intx()](#Vector2dintx)
- [inty()](#Vector2dinty)
- [to_angle()](#Vector2dto_angle)
- [rounded()](#Vector2drounded)
- [fast_reach_test()](#Vector2dfast_reach_test)
- [get_quarter()](#Vector2dget_quarter)
- [is_in_box()](#Vector2dis_in_box)
- [is_gaussean()](#Vector2dis_gaussean)
- [complex_multiply()](#Vector2dcomplex_multiply)
- [dot_multiply()](#Vector2ddot_multiply)

<br>

**Arguments:**
- x (float) <br> float representing x coordinate. Default 0
- y (float) <br> float representing y coordinate. Default 0

**Returns:**
- newly created *Vector2d* object.

**Variables:**
- x (float) <br> float representing x coordinate
- y (float) <br> float representing y coordinate

**Operations:**
- **addition**:<br> Vector2d(a, b) + Vector2d(c, d) -> Vector2d(a + c, b + d)
- **substraction**:<br> Vector2d(a, b) - Vector2d(c, d) -> Vector2d(a - c, b - d)
- **multiplication**:<br> Vector2d(a, b) * Vector2d(c, d) -> Vector2d(a * c, b * d) <br> Vector2d(a, b) * c -> Vector2d(a * c, b * c)
- **true division**:<br> Vector2d(a, b) / Vector2d(c, d) -> Vector2d(a / c, b / d) <br> Vector2d(a, b) / c -> Vector2d(a / c, b / c) 
- **floor division**:<br> Vector2d(a, b) // Vector2d(c, d) -> Vector2d(a // c, b // d) <br> Vector2d(a, b) // c -> Vector2d(a // c, b // c)
- **module division**:<br> Vector2d(a, b) % Vector2d(c, d) -> Vector2d(a % c, b % d) <br> Vector2d(a, b) % c -> Vector2d(a % c, b % c)
- **is equal**:<br> Vector2d(a, b) == Vector2d(c, d) -> (a == c) and (b == d)
- **is not equal**:<br> Vector2d(a, b) != Vector2d(c, d) -> (a != c) or (b != d)
- **get item**:<br> Vector2d(a, b)\[i] -> (a, b)\[i]
> [!NOTE]
> when getting items, index i must be 0 or 1

### Vector2d.from_tuple()
Vector2d.from_tuple(tpl: tuple\[float, float]) -> Vector2d
Static method. Creates new Vector2d using tuple. x, y = tpl

### Vector2d.as_tuple()
Vector2d.as_tuple() -> tuple\[float, float]
returns tuple (x, y).

### Vector2d.distance()
Vector2d.distance(other: Vector2d) -> float
returns euclidic length of vectors' differences.
distance<sup>2</sup> = (x<sub>1</sub> - x<sub>2</sub>)<sup>2</sup> + (y<sub>1</sub> - y<sub>2</sub>)<sup>2</sup>

### Vector2d.length()
Vector2d.length() -> float
returns euclidic length of vetor.
length<sup>2</sup> = x<sup>2</sup> + y<sup>2</sup>

### Vector2d.norm()
Vector2d.norm() -> Vector2d
returns normalized (length = 1) Vector2d with same direction.
if Vector2d is **0**, returns **0**

### Vector2d.intx()
Vector2d.intx() -> int
returns int(x)

### Vector2d.inty()
Vector2d.inty() -> int
returns int(y)

### Vector2d.to_angle()
Vector2d.to_angle() -> Angle
returns angle of vector using arc tangent.

### Vector2d.rounded()
Vector2d.rounded(ndigits: int = None) -> Vector2d
returns Vector with x and y rounded to given n digits.

### Vector2d.fast_reach_test()
Vector2d.fast_reach_test(other: Vector2d, dist: float) -> bool
checks if distance between vectors is smaller than dist.

### Vector2d.getQuarter()
Vector2d.getQuarter() -> int.
returns plane quarter of vector.

| **2** | **1** |
| ----- | ----- |
| **3** | **4** |

### Vector2d.is_in_box()
Vector2d.is_in_box(other1: Vector2d, other2: Vector2d) -> bool
returns True if **self** is in rect such that **other1** and **other2** are corners.

### Vector2d.is_gaussean()
Vector2d.is_gaussean() -> bool
returns True if both *x* and *y* variables are integers.

### Vector2d.complex_multiply()
Vector2d.complex_multiply(other: Vector2d) -> Vector2d
multiplies vectors as if Vector2d(a, b) = a + bi.
resulting **vector**'s length is product of **self** and **other** lengths.
resulting **vector**'s angle is sum of **self** and **other** angles.

### Vector2d.dot_multiply()
Vector2d.dot_multiply(other: Vector2d) -> float
returns value of dot multiplication of vectors.
resulting value is product of **self** and **other** lengths with cosine of angle between **self** and **other**.

### Vector2d.operation()
Vector2d.operation(other: Vector2d, operation: Callable\[\[float, float], float]) -> Vector2d
returns vector such that its coords are operation(self.coord, other.coord)

---

# VectorRange
class to represent a range of gaussean (integer) vectors.

> VectorRenge(end: Vector2d) -> VectorRange
> VectorRenge(start: Vector2d, end: Vector2d) -> VectorRange
> VectorRenge(start: Vector2d, end: Vector2d, step: Vector2d) -> VectorRange

<br>

**Arguments:**
- start (Vector2d) <br> start vector of the range. Initially Vector2d(0, 0).
- end (Vector2d) <br> end vector of the range.
- step (Vector2d) <br> step vector of the range. Initially Vector2d(1, 1).
> [!NOTE]
> All arguments must be gausseans, and it must be possible to get from start to end using *step* * *k* where k is gaussean, k.x > 0, and k.y > 0

**Returns:**
- newly created *VectorRange* object.

**Variables:**
- start (Vector2d) <br> start vector of the range.
- end (Vector2d) <br> end vector of the range.
- step (Vector2d) <br> step vector of the range.
- steps (Vector2d) <br> vector of steps to reach the end
> [!NOTE]
> *steps* variable is such a k vector discussed in note above.

**Operations:**
- get item:<br> returns Vector2d according to range. It will go first on x axis, and then on y axis.
> [!NOTE]
> For example, in VectorRange(Vector2d(3, 2)) it will go as:
> | **0** | **1** | **2** |
> | ----- | ----- | ----- |
> | **3** | **4** | **5** |
> 
> the order will be: <0, 0>, <1, 0>, <2, 0>, <0, 1>, <1, 1>, <2, 1>


---

# Angle

class that represent angles in radians.

> Angle() -> Angle
> Angle(angle: float) -> Angle

- [set()](Angleset)
- [get()](Angleget)
- [bound()](Anglebound)
- [to_vector2d()](Angleto_vector2d)
<br>

**Arguments:**
- angle (float) <br> angle in radians. Default 0

**Returns:**
- newly created *Angle* object.

**Variables:**
- angle (float) <br> angle in radians.

**Operations:**
- addition:<br> Angle(a) + Angle(b) = Angle((a + b) % (2 * pi))
- substraction:<br> Angle(a) - Angle(b) = Angle((a - b) % (2 * pi))

### Angle.set()
Angle.set(angle: float, is_deegre: bool) -> None
sets the angle value equal to given. if is_degree is True, changes angle to radians

### Angle.get()
Angle.get(is_degree: bool) -> float
returns value of angle. if is_degree is True, returns it in degrees rather than in radians

### Angle.bound()
Angle.bound() -> None
module divides angle by 2pi

### Angle.toVector2d()
Angle.to_vector2d() -> Vector2d
returns Vector2d with length equal to 1 and direction equal to angle

---

# Tips

### 1. Use chunks

since 0.0.7 update every game object which has need_blit equal true and whose surface does not *touch* the camera view, is checked to *touch* the camera view every frame. Thus, if there is a lot of game objects outside of camera view, or just very far away, it is better to create a *chunk* game object that will contain other game objects as its childs. This is computationaly easier because now engine will check only if it *touches* the chunk.

#### Example:

```py
from src.engine_antiantilopa import *


# Create Engine with 700x500 window
e = Engine(Vector2d(700, 500))
e.set_debug(1)

# Bind keys for movement of camera (Default wasd)
bind_keys_for_camera_movement()

# Create Game object with Coords <0, 0> and surface 500x500
world = GameObject("world")
world.add_component(Transform(Vector2d(0, 0)))
world.add_component(SurfaceComponent(Vector2d(1500, 1500)))
GameObject.root.add_child(world)

# Create 16 x 16 chunks each containing 16 x 16 buttons
for i in range(16):
    for j in range(16):
        chunk = GameObject(["chunk", f"{i}/{j}"])
        chunk.add_component(Transform(Vector2d(i * 3 * 16 - (256 * 3 / 2), j * 3 * 16 - (256 * 3 / 2))))
        chunk.add_component(SurfaceComponent(Vector2d(3 * 16 + 2, 3 * 16 + 2)))
        # in Vector2d(3 * 16 + 2, 3 * 16 + 2)),  '+ 2' part is needed for the upper and left border of the chunk. 
        # However, I don't know why it is so.
        world.add_child(chunk)
# Create 256 x 256 buttons
for i in range(256):
    for j  in range(256):
        button = GameObject("button")

        button.add_component(RectShapeComponent(Vector2d(2, 2)))
        button.add_component(Transform(Vector2d((i % 16) * 3 - 3 * 8, (j % 16) * 3 - 3 * 8)))
        button.add_component(ColorComponent((i % 256, j % 256, 128)))
        button.add_component(SurfaceComponent(Vector2d(2, 2), 1))

        # Find to which chunk the button is assigned to
        ch = GameObject.get_group_by_tag(f"{i // 16}/{j // 16}")[0]
        ch.add_child(button)

#run engine
e.run(120)
```

and I (on my relatively good laptop) got approximately ```fps = 17.5``` (0.0.7) which is (in my opinion) good result for python code. Try to launch code without chunk separation

### 2. Blit game objects from the start

Another way to tackle the issue mentioned in first tip, is blit all game objects on start, so the loading of programm is little bit slower, but frame rate is higher. This, however, works only if objects are static (need_blit = False and almost never a lot of them get True). 

#### Example:

```py
from src.engine_antiantilopa import *


# Create Engine with 700x500 window
e = Engine(Vector2d(700, 500))
e.set_debug(1)

# Bind keys for movement of camera (Default wasd)
bind_keys_for_camera_movement()

# Create Game object with Coords <0, 0> and surface 500x500
world = GameObject("world")
world.add_component(Transform(Vector2d(0, 0)))
world.add_component(SurfaceComponent(Vector2d(1500, 1500)))
world.add_component(RectShapeComponent(Vector2d(1500, 1500), need_draw=False))
GameObject.root.add_child(world)

# Create 256 x 256 buttons
for i in range(256):
    for j  in range(256):
        button = GameObject("button")

        button.add_component(RectShapeComponent(Vector2d(2, 2)))
        button.add_component(Transform(Vector2d(i * 3 - 128 * 3, j * 3 - 128 * 3)))
        button.add_component(ColorComponent((i % 256, j % 256, 128)))
        button.add_component(SurfaceComponent(Vector2d(2, 2), 1))
        # Find to which chunk the button is assigned to
        world.add_child(button)

e.draw()
e.forced_blit()

#run engine
e.run(120)
```

Its results as ```fps = 22``` (0.0.7) is very good, but it works only because there is no animation or other thing on those game objects. It is highly recommended to use first tip anyway. It is also possible to use first and second tips together.

### 3. Assign the least number of OnClickComponents 

If you have a lot of buttons in some pattern, it is much better to wrap them in one game object and add on click component only to it, with checking which button was clicked in function (cmd) itself. It is possible since 0.0.7 when *mouse_pos* argument to cmd was added. This is computationaly easier because after click, engine will check only one game object for interceptoin, not a big amount.

#### Example:

```py
from src.engine_antiantilopa import *


# Create Engine with 700x500 window
e = Engine(Vector2d(700, 500))

# Bind keys for movement of camera (Default wasd)
bind_keys_for_camera_movement()

# Create Game object with Coords <0, 0> and surface 500x500
world = GameObject("world")
world.add_component(Transform(Vector2d(0, 0)))
world.add_component(SurfaceComponent(Vector2d(1500, 1500)))
world.add_component(RectShapeComponent(Vector2d(1500, 1500), need_draw=False))

# create cmd where we check where on world the mouse is clicked.
def cmd(game_object: GameObject, active_keys: tuple[int, int, int], mouse_pos: Vector2d, *args):
    print(f"color = <{int(mouse_pos.x // 3 + 128)}, {int(mouse_pos.y // 3 + 128)}, {128}>")

world.add_component(OnClickComponent((1, 0, 0), 1, 0, cmd))

GameObject.root.add_child(world)

# Create 256 x 256 buttons
for i in range(256):
    for j  in range(256):
        button = GameObject("button")

        button.add_component(RectShapeComponent(Vector2d(2, 2)))
        button.add_component(Transform(Vector2d(i * 3 - 128 * 3, j * 3 - 128 * 3)))
        button.add_component(ColorComponent((i % 256, j % 256, 128)))
        button.add_component(SurfaceComponent(Vector2d(2, 2), 1))
        # Find to which chunk the button is assigned to
        world.add_child(button)

#run engine
e.run(120)
```

As it could be seen, after a click, there is no freezes that would occur when clicked.