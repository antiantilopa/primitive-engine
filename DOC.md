# Primitive engine 

Welcome to Primitive engine documentation!

Primitive engine is based on pygame_tools_tafh module, and is written on python as a wrapper for pygame module.

---

# Example

It is example of red circle object on the screen

```py
from engine import *

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

button.add_component(CircleComponent(100))
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
- [Engine](#Engine)
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
- [Vector Math](#vector-math)
- - [Vector2d](#vector2d)
- - [Angle](#angle)
---

# Engine

main object of programm
> Engine() -> Engine
> Engine(window_size: Vector2d) -> Engine

- [draw()](#enginedraw)
- [iteration()](#engineiteration)
- [run()](#enginerun)
- [update()](#engineupdate)
<br>
The *Engine* class gathers and launches all code at once. Default init creates window size equal to size of display.

**Arguments:**
- window_size (Vector2d | tuple[int, int]) <br> size of created window.

**Returns:**
- newly created *Engine* object.

**Variables:**
- no parameters

### Engine.iteration()
Engine.iteration() -> None
calls [iteration()](#game-objectiteration) method from all [game objects](#game-object)

### Engine.draw()
Engine.draw() -> None
calls [draw()](#game-objectdraw) method from all game objects and blit all surfaces according to geneology tree

### Engine.update()
Engine.update() -> None
calls [update()](#game-objectupdate) methos from all game objects

### Engine.run()
Engine.run() -> None
runs pygame application in a loop until window quit or error occur

---

# Game Object

object for all game "objects"
> GameObject() -> GameObject
> GameObject(tags: str) -> GameObject
> GameObject(tags: list\[str]) -> GameObject

- [get_group_by_tag()](#gameobjectget_group_by_tag)
- [add_component()](#gameobjectadd_component)
- [add_child()](#gameobjectadd_child)
- [get_component()](#gameobjectget_component)
- [contains_component()](#gameobjectcontains_component)
- [get_childs()](#gameobjectget_childs)
- [iteration()](#gameobjectiteration)
- [draw()](#gameobjectdraw)
- [update()](#gameobjectupdate)
- [enable()](#gameobjectenable)
- [disable()](#gameobjectdisable)
- [destroy()](#gameobjectdestroy)
- [show_geneology_tree()](#gameobjectshow_geneology_tree)
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

**Static Variables:**
- root ([GameObject](#game-object)) <br> root game object representing screen. all gameobject have to be chained to it to be drawn. 
- objs (list\[[GameObject](#game-object)]) <br> all initialized game objects list. Initially empty
- group_tag_dict (dict\[str, [GameObject](#game-object)]) <br> dictionary of tags to game objects. Initially empty.

### GameObject.get_group_by_tag()
GameObject.get_group_by_tag(tag: str) -> list\[[GameObject](#game-object)]
Static method. returns all game objects with given tag

### GameObject.show_geneology_tree()
show_geneology_tree(game_object: "[GameObject](#game-object)|None" = None, depth: int = 1) -> None
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
returns all childs of the components with a given tag

### GameObject.iteration()
GameObject.iteration() -> None
calls iteration() method for all components of the game object

### GameObject.draw()
GameObject.draw() -> None
calls draw() method for all components of the game object

### GameObject.update()
GameObject.update() -> None
calls iteration() and draw() methods for all components of the game object

### GameObject.enable()
GameObject.enable() -> None
sets acrive variable equal to True and enables all game objects chained to this game object.

### GameObject.disable()
GameObject.disable() -> None
sets acrive variable equal to False and disables all game objects chained to this game object.

### GameObject.destroy()
GameObject.destroy() -> None
destroys game object and all childs and components of the game object. Removes it from tag dictionary, objs list, and parents' childs list.  

---

# Component
base class for other components in game. Not used directly.
> Component() -> Component

- [iteration()](#componentiteration)
- [draw()](#componentdraw)
<br>

**Arguments:**
- no arguments

**Returns:**
- no returns

**variables:**
- game_object ([GameObject](#game-object)) <br> game_object that contains the component

### Component.iteration()
Component.iteration() -> None
does nothing

### Component.draw()
Component.draw() -> None
does nothing

---

# Transform
Child class of [Component](#component).
object for representing position and rotation in 2 dimensions.
> Transform() -> Transform
> Transform(pos: Vector2d) -> Transform
> Transform(rotation: Angle|float) -> Transform
> Transform(pos: Vector2d, rotation: Angle|float) -> Transform

- [move()](#transformmove)
- [rotate()](#transformrotate)
- [set_pos()](#transformset_pos)
- [set_rotation](#transformset_rotation)
<br>

**Arguments:**
- pos (Vector2d) <br> position of the **center** of the game object.
- rotation (Angle | float) <br> angle of the gameobject. ***Not working now!!!***

**Returns:**
- newly created Transform component.

**Variables:**
- pos (Vector2d) <br> position of the **center** of the game object.
- rotation (Angle) <br> angle of the gameobject.

### Transform.move()
Transform.move(delta: Vector2d) -> None
changes position with given delta.

### Transform.rotate()
Transform.rotate(delta: Angle) -> None
changes rotation with given delta

### Transform.set_pos()
Transform.set_pos(pos: Vector2d) -> None
sets position equal to pos

### Transform.set_rotation()
Transform.set_rotation(rotation: Angle) -> None
sets (self.)rotation equal to given rotation

---

# Surface Component
Child class of [Component](#component).
object for representing surface where everything is drawn.
> SurfaceComponent(size: Vector2d) -> SurfaceComponent

- [blit()](#surfacecomponentblit)
<br>

**Requirements:**
- [Transform Component](#transform)
- parent with Surface Component

**Arguments:**
- size (Vector2d) <br> size of surface and game object.

**Returns:**
- newly created *SurfaceComponent* object.

**Variables:**
- size: Vector2d <br> size of surface and game object.
- pg_surf: pygame.Surface <br> actual pygame surface where child game objects will be drawn

### SurfaceComponent.blit()
SurfaceComponent.blit() -> None
blits the surface to parent surface.
if game object is root, nothing happens. (because root has not parent game object)

---

# Color Component
child class of [Component](#component).
object for representation of color in RGB.

> ColorComponent(color: tuple\[int, int, int]) -> ColorComponent

**Arguments:**
- color (tuple\[int, int, int]) <br> RGB color of game object. each number must be in range (0, 256).

**Returns:**
- newly created *ColorComponent* object

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

- [does_collide()](#circleshapecomponentdoes_collide)
- [draw()](#circleshapecomponentdraw)
<br>

**Requirements:**
- [Transform Component](#transform)
- [Surface Component](#surface-component) (if contains [Color Component](#color-component))

**Arguments:**
- radius (float) <br> radius of issued circle shape

**Returns:**
- newly created *CircleShapeComponent* object

**Variables:**
- radius (float) <br> radius of issued circle shape

### CircleShapeComponent.does_collide()
CircleShapeComponent.does_collide(pos: Vector2d) -> bool
check if given pos lies in circle centered in transform, with known radius.

### CircleShapeComponent.draw()
CircleShapeComponent.draw() -> None
if game object contains [Color Component](#color-component), draws circle centered in transform, with known radius and color.

---

# Rect Shape Component
Child class of [ShapeComponent](#shape-component).
represent rectangle shape.
> RectShapeComponent(size: Vector2d) -> RectShapeComponent

- [does_collide()](#rectshapecomponentdoes_collide)
- [draw()](#rectshapecomponentdraw)
<br>

**Requirements:**
- [Transform Component](#transform)
- [Surface Component](#surface-component) (if contains [Color Component](#color-component))

**Arguments:**
- size (Vector2d) <br> width and height of issued rectangle shape

**Returns:**
- newly created *RectShapeComponent* object

**Variables:**
- size (Vector2d) <br> width and height of issued rectangle shape

### RectShapeComponent.does_collide()
RectShapeComponent.does_collide(pos: Vector2d) -> bool
check if given pos lies in rectangle centered in transform, with known width and height.

### RectShapeComponent.draw()
RectShapeComponent.draw() -> None
if game object contains [Color Component](#color-component), draws rectangle centered in transform, with known width, height, and color.

---

# On Click Component
Child class of [Component](#component).
object for listening for mouse clicks and responding to them.
> OnClickComponent(listen: tuple\[bool, bool, bool], listen_for_hold: bool, on_press: bool, cmd: Callable\[\[[GameObject](#game-object), tuple\[bool, bool, bool]], None]) -> OnClickComponent

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
- cmd (Callable\[\[[GameObject](#game-object), tuple\[bool, bool, bool]], None]) <br> callable function which will be called when mouse button pressed and all requirements satisfied. First argument - game object whose OnliclkComponent was triggered; Second argument - tuple\[bool, bool, bool] which mouse button (left, center or right) triggered OnliclkComponent.

**Returns:**
- newly created *OnClickComponent* object.

**Variables:**
- listen (tuple\[bool, bool, bool]) <br> tuple of 3 booleans each representing whether or not should it be listened for left, center, or right mouse buttons respectively.
- listen_for_holds (bool) <br> boolean representing should it be triggered by mouse buttons changes (False) or it being held (True).
- on_press (bool) <br> boolean representing should it be triggered by mouse button release (False) or mouse button push (True). Does not affect if listen_for_holds is True
- cmd (Callable\[\[[GameObject](#game-object), tuple\[bool, bool, bool]], None]) <br> callable function which will be called when mouse button pressed and all requirements satisfied. First argument - game object whose OnliclkComponent was triggered; Second argument - tuple\[bool, bool, bool] which mouse button (left, center or right) triggered OnliclkComponent.
- previous (tuple\[bool, bool, bool]) <br> tuple of 3 booleans each representing mouse buttons state at previous iteration. *It is not updated if listen_for_holds is False*.

### OnClickComponent.iteration()
OnClickComponent.iteration() -> None
check if triggered, and if it is, call cmd(self.game_object, mouse_buttons)
also checks if mouse position lies in game object's shape

### OnClickComponent.get_relative_coord()
OnClickComponent.get_relative_coord(pos: Vector2d) -> Vector2d
gets absolute position on actual screen/display and returns position relative to the game object's center

---

# Key Bind Component
Child class of [Component](#component).
object for listening for keyboard clicks and responding to them.
> KeyBindComponent(listen: tuple\[int], listen_for_hold: bool, on_press: bool,  cmd: Callable\[\[[GameObject](#game-object), tuple\[int]], None]) -> KeyBindComponent

- [iteration()](#keybindcomponentiteration)
<br>

**Arguments:**
- listen (tuple\[int]) <br> tuple of integers each representing whether or not should it be listened for keyboard keys according to pygame keys indexation.
- listen_for_holds (bool) <br> boolean representing should it be triggered by keyboard keys changes (False) or they being held (True).
- on_press (bool) <br> boolean representing should it be triggered by keyboard keys releases (False) or their pushes (True). Does not affect if listen_for_holds is True
- cmd (Callable\[\[[GameObject](#game-object), tuple\[int]], None]) <br> callable function which will be called when keyboard keys pressed and all requirements satisfied. First argument - game object whose KeyBindComponent was triggered; Second argument - tuple\[int] which keyboard keys (according to pygame keys indexation) triggered KeyBindComponent.

**Returns:**
- newly created *KeyBindComponent* object.

**Variables:**
- listen (tuple\[int]) <br> tuple of integers each representing whether or not should it be listened for keyboard keys according to pygame keys indexation.
- listen_for_holds (bool) <br> boolean representing should it be triggered by keyboard keys changes (False) or they being held (True).
- on_press (bool) <br> boolean representing should it be triggered by keyboard keys releases (False) or their pushes (True). Does not affect if listen_for_holds is True
- cmd (Callable\[\[[GameObject](#game-object), tuple\[int]], None]) <br> callable function which will be called when keyboard keys pressed and all requirements satisfied. First argument - game object whose KeyBindComponent was triggered; Second argument - tuple\[int] which keyboard keys (according to pygame keys indexation) triggered KeyBindComponent.
- previous (list\[int]) <br> tuple of integers each representing keyboard keys states at previous iteration. *It is not updated if listen_for_holds is False*.
 
### KeyBindComponent.iteration()
KeyBindComponent.iteration() -> None
check if triggered, and if it is, calls cmd(self.game_object, keyboard_keys)

---

# Label Component
Child class of [Component](#component).
object for text render.
> LabelComponent(text: str) -> LabelComponent
> LabelComponent(text: str, font: pygame.font.Font) -> LabelComponent

- [draw()](#labelcomponentdraw)
<br>

**Requirements:**
- [Transform Component](#transform)
- [Color Component](#color-component)
- [Surface Component](#surface-component)

**Arguments:**
- text (str) <br> string that will be drawn. cannot have any esc commands. does not support \\n (next line).
- font (pygame.font.Font) <br> font that will be used to draw text. Initially is "Consolas" font.

**Returns:**
- newly created *LabelComponent* object

**Variables:**
- text (str) <br> string that will be drawn. cannot have any esc commands. does not support \\n (next line).
- font (pygame.font.Font) <br> font that will be used to draw text. Initially is "Consolas", px =30 font. 

### LabelComponent.draw()
LabelComponent.draw() -> None
blits text on the surface.

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
- [lenght()](#Vector2dlenght)
- [norm()](#Vector2dnorm)
- [intx()](#Vector2dintx)
- [inty()](#Vector2dinty)
- [to_angle()](#Vector2dto_angle)
- [rounded()](#Vector2drounded)
- [fast_reach_test()](#Vector2dfast_reach_test)
- [get_quarter()](#Vector2dget_quarter)
- [is_in_box()](#Vector2dis_in_box)
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
- addition:<br> Vector2d(a, b) + Vector2d(c, d) -> Vector2d(a + c, b + d)
- substraction:<br> Vector2d(a, b) - Vector2d(c, d) -> Vector2d(a - c, b - d)
- multiplication:<br> Vector2d(a, b) * Vector2d(c, d) -> Vector2d(a * c, b * d) <br> Vector2d(a, b) * c -> Vector2d(a * c, b * c)
- true division:<br> Vector2d(a, b) / c -> Vector2d(a / c, b / c)
- floor division:<br> Vector2d(a, b) // c -> Vector2d(a // c, b // c)
- module division:<br> Vector2d(a, b) % c -> Vector2d(a % c, b % c)
- is equal:<br> Vector(a, b) == Vector(c, d) -> (a == c) and (b == d)
- is not equal:<br> Vector(a, b) != Vector(c, d) -> (a != c) or (b != d)

### Vector2d.from_tuple()
Vector2d.from_tuple(tpl: tuple\[float, float]) -> Vector2d
Static method. Creates new Vector2d using tuple. x, y = tpl

### Vector2d.as_tuple()
Vector2d.as_tuple() -> tuple\[float, float]
returns tuple (x, y).

### Vector2d.distance()
Vector2d.distance(other: Vector2d) -> float
returns euclidic lenght of vectors' differences.
d<sup>2</sup> = x<sup>2</sup> + y<sup>2</sup>

### Vector2d.lenght()
Vector2d.lenght() -> float
returns euclidic lenght of vetor.
d<sup>2</sup> = x<sup>2</sup> + y<sup>2</sup>

### Vector2d.norm()
Vector2d.norm() -> Vector2d
returns normalized (lenght = 1) Vector2d with same direction.
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

### Vector2d.complex_multiply()
Vector2d.complex_multiply(other: Vector2d) -> Vector2d
multiplies vectors as if Vector2d(a, b) = a + bi.
resulting **vector**'s lenght is product of **self** and **other** lenghts.
resulting **vector**'s angle is sum of **self** and **other** angles.

### Vector2d.dot_multiply()
Vector2d.dot_multiply(other: Vector2d) -> float
returns value of dot multiplication of vectors.
resulting value is product of **self** and **other** lenghts with cosine of angle between **self** and **other**.

### Vector2d.operation()
Vector2d.operation(other: Vector2d, operation: Callable\[\[float, float], float]) -> Vector2d
returns vector such that its coords are operation(self.coord, other.coord)

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
- newly created *Angle* object

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
returns Vector2d with lenght equal to 1 and direction equal to angle

---
