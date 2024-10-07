User question: what task or tasks did you perform when you toggle on the faucet?

[...]

>>> history.search("toggle on the faucet")

[
0: 2023/04/24 09:50:27 - 09:50:40: """Goal: ToggleOff(Faucet)
  Visual observation: Apple_1, Tomato_2, Mug_1 [filled], StoveBurner_0, StoveBurner_2, Drawer_1, Cabinet_3, Cabinet_5, Cabinet_6, Cabinet_10, StoveKnob_0, StoveKnob_1, StoveKnob_2 [toggled], StoveKnob_3 [toggled], Pan, Microwave, Faucet [toggled], Sink_Basin
  Mug_1, Tomato_2, Apple_1 are in/on Sink_Basin"""  
  ...
1: 2023/04/24 09:50:43 - 09:50:52: """Goal: Pickup(Tomato_1)
  Visual observation: Tomato_1, DiningTable_0, Floor
  DiningTable_0 is in/on Floor
  Speech:
  2023-04-24 09:50:51.759249: put all 3 spatulas in one cabinet"""  
  ...
...
35: 2023/04/25 11:10:03 - 11:10:03: """Goal: ToggleOn(Faucet)
  Visual observation: PepperShaker_1, Cabinet_2, Cabinet_3, Cabinet_4, Cabinet_5, Cabinet_6, Cabinet_18, Drawer_0, Sink, CounterTop_2, Pan, Apple, Spatula, Sink_Basin, Potato, Mug [dirty], Faucet
  Potato, Apple, Spatula, PepperShaker_1, Pan are in/on CounterTop_2
  Faucet, Mug are in/on Sink_Basin"""  
  ...
36: 2023/04/25 11:10:08 - 11:10:08: """Goal: ToggleOff(Faucet)
  Visual observation: PepperShaker_1, Cabinet_2, Cabinet_3, Cabinet_4, Cabinet_5, Cabinet_6, Cabinet_18, Drawer_0, Sink, CounterTop_2, Pan, Apple, Spatula, Sink_Basin, Potato, Mug [filled], Faucet [toggled]
  Potato, Apple, Spatula, PepperShaker_1, Pan are in/on CounterTop_2
  Faucet, Mug are in/on Sink_Basin"""  
  ...
37: 2023/04/25 11:10:11 - 11:10:11: """Goal: Pickup(Mug)
  Visual observation: PepperShaker_1, Cabinet_2, Cabinet_3, Cabinet_4, Cabinet_5, Cabinet_6, Cabinet_18, Drawer_0, Sink, CounterTop_2, Pan, Apple, Spatula, Sink_Basin, Potato, Mug [filled], Faucet [toggled]
  Potato, Apple, Spatula, PepperShaker_1, Pan are in/on CounterTop_2
  Faucet, Mug are in/on Sink_Basin"""  
  ...
38: 2023/04/25 11:10:14 - 11:10:14: """Goal: Pour(Sink_Basin)
  Visual observation: PepperShaker_1, Cabinet_2, Cabinet_3, Cabinet_4, Cabinet_5, Cabinet_6, Cabinet_18, Drawer_0, Sink, CounterTop_2, Pan, Apple, Spatula, Sink_Basin, Potato, Mug [filled], Faucet [toggled], agent hand
  Potato, Apple, Spatula, PepperShaker_1, Pan are in/on CounterTop_2
  Faucet is in/on Sink_Basin
  Mug is inside agent hand"""  
  ...
39: 2023/04/25 11:10:23 - 11:10:34: """Goal: Place(CoffeeMachine)
  Visual observation: CoffeeMachine, Cup [dirty, filled], Mug [filled], CounterTop_2, PepperShaker_1, CounterTop_1, Apple, agent hand
  Cup, CoffeeMachine are in/on CounterTop_1
  Mug is inside agent hand
  PepperShaker_1, Apple are in/on CounterTop_2"""  
  ...
...
66: 2023/04/25 11:17:59 - 11:18:07: """Goal: Pickup(Apple)
  Visual observation: Cabinet_2, Cabinet_3, Cabinet_5, Cabinet_6, Cabinet_17, Cabinet_18, Sink, CounterTop_2, Apple, Sink_Basin, Potato, Microwave, Faucet [toggled], Plate_0, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Fridge [open], Spoon_2, PepperShaker_1, CounterTop_1, Egg, Knife_0, CoffeeMachine [toggled], Mug [filled]
  Spoon_2 is in/on Fridge
  Plate_0, Bread_0_Sliced_3, Egg, Bread_0_Sliced_2, Knife_0 are in/on CounterTop_1
  Mug is in/on CoffeeMachine
  Apple, Microwave, PepperShaker_1, Potato are in/on CounterTop_2
  Bread_0_Sliced_2, Bread_0_Sliced_3 are in/on Plate_0
  Faucet is in/on Sink_Basin"""  
  ...
67: 2023/04/25 11:18:12 - 11:18:12: """Goal: Place(CounterTop_2)
  Visual observation: Cabinet_2, Cabinet_3, Cabinet_5, Cabinet_6, Cabinet_17, Cabinet_18, Sink, CounterTop_2, Apple, Sink_Basin, Potato, Microwave, Faucet [toggled], Plate_0, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Fridge [open], Spoon_2, PepperShaker_1, CounterTop_1, agent hand, Egg, Knife_0, CoffeeMachine [toggled], Mug [filled]
  Spoon_2 is in/on Fridge
  Plate_0, Bread_0_Sliced_3, Bread_0_Sliced_2, Egg, Knife_0 are in/on CounterTop_1
  Bread_0_Sliced_2, Bread_0_Sliced_3 are in/on Plate_0
  Mug is in/on CoffeeMachine
  Microwave, PepperShaker_1, Potato are in/on CounterTop_2
  Faucet is in/on Sink_Basin
  Apple is inside agent hand"""  
  ...
68: 2023/04/25 11:18:13 - 11:18:20: """Goal: Open(Microwave)
  Visual observation: Plate_1 [dirty], Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_11, Cabinet_16, CounterTop_2, Drawer_2, Potato, Microwave, Plate_0, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Fridge [open], Spoon_2, PepperShaker_1, CounterTop_1, Apple, Egg, Knife_0, CoffeeMachine [toggled], Mug [filled]
  Plate_0, Bread_0_Sliced_3, Egg, Knife_0, Bread_0_Sliced_2 are in/on CounterTop_1
  Plate_1, PepperShaker_1, Apple, Potato, Microwave are in/on CounterTop_2
  Bread_0_Sliced_3, Bread_0_Sliced_2 are in/on Plate_0
  Mug is in/on CoffeeMachine
  Spoon_2 is in/on Fridge"""  
  ...
...
78: 2023/04/25 14:23:22 - 14:23:47: """Goal: ToggleOff(Faucet_1)
  Visual observation: Cabinet_8, Curtains, Fork_0, Knife, Tomato_0, ButterKnife, CoffeeMachine, Faucet_0, Faucet_1 [toggled], CounterTop_0, Sink_Basin
  ButterKnife, Faucet_1, CoffeeMachine, Faucet_0 are in/on CounterTop_0
  Tomato_0, Fork_0, Knife are in/on Sink_Basin
  Speech:
  2023-04-25 14:23:27.067196: Hello!
  2023-04-25 14:23:39.112014: You need to place all the tomatoes into one cabinet.
  2023-04-25 14:23:46.395151: There is a tomato in the sink."""  
  ...
...
92: 2023/04/26 15:04:44 - 15:04:44: """Goal: ToggleOn(CoffeeMachine)
  Visual observation: Potato_1, Sink, CounterTop_0, Cabinet_3, Cabinet_6, Cabinet_7, Cabinet_10, Cabinet_11, Fork, Window_0, WineBottle_0, Plate [dirty], Sink_Basin, ButterKnife, DishSponge, Apple, CoffeeMachine, Mug, Faucet
  Mug is in/on CoffeeMachine
  ButterKnife, DishSponge, Mug, Apple, CoffeeMachine, Sink are in/on CounterTop_0
  WineBottle_0, Plate, Faucet are in/on Sink"""  
  ...
...
117: 2023/04/26 15:09:26 - 15:09:26: """Goal: ToggleOn(Faucet)
  Visual observation: Potato_1, Sink, StoveBurner_0, CounterTop_0, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, StoveBurner_3, Fork, Window_0, WineBottle_0, Plate [dirty], Potato_0, Sink_Basin, SaltShaker, DishSponge, Apple, Pan_0 [dirty], CoffeeMachine [toggled], SoapBottle, Faucet, DiningTable, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, Floor, ButterKnife, Mug [filled]
  Potato_1, Tomato_1_Sliced_0, Fork, DishSponge, CoffeeMachine, Sink, Potato_0, Apple, ButterKnife are in/on CounterTop_0
  Tomato_1_Sliced_1, Tomato_1_Sliced_2 are in/on DiningTable
  DiningTable is in/on Floor
  Plate is in/on Sink_Basin
  Mug is in/on CoffeeMachine
  Faucet, WineBottle_0, SoapBottle are in/on Sink"""  
  ...
118: 2023/04/26 15:09:31 - 15:09:31: """Goal: ToggleOff(Faucet)
  Visual observation: Potato_1, Sink, StoveBurner_0, CounterTop_0, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, StoveBurner_3, Fork, Window_0, WineBottle_0 [filled], Plate, Potato_0, Sink_Basin, SaltShaker, DishSponge, Apple, Pan_0 [dirty], CoffeeMachine [toggled], SoapBottle, Faucet [toggled], DiningTable, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, Floor, ButterKnife, Mug [filled]
  Potato_1, Tomato_1_Sliced_0, Fork, DishSponge, CoffeeMachine, Sink, Potato_0, Apple, ButterKnife are in/on CounterTop_0
  Tomato_1_Sliced_1, Tomato_1_Sliced_2 are in/on DiningTable
  DiningTable is in/on Floor
  Plate is in/on Sink_Basin
  Mug is in/on CoffeeMachine
  Faucet, WineBottle_0, SoapBottle are in/on Sink"""  
  ...
119: 2023/04/26 15:09:37 - 15:09:37: """Goal: Pickup(Plate)
  Visual observation: Potato_1, Sink, StoveBurner_0, CounterTop_0, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, StoveBurner_3, Fork, Window_0, WineBottle_0 [filled], Plate, Potato_0, Sink_Basin, SaltShaker, DishSponge, Apple, Pan_0 [dirty], CoffeeMachine [toggled], SoapBottle, Faucet [toggled], DiningTable, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, Floor, ButterKnife, Mug [filled]
  Potato_1, Tomato_1_Sliced_0, Fork, DishSponge, CoffeeMachine, Sink, Potato_0, Apple, ButterKnife are in/on CounterTop_0
  Tomato_1_Sliced_1, Tomato_1_Sliced_2 are in/on DiningTable
  DiningTable is in/on Floor
  Plate is in/on Sink_Basin
  Mug is in/on CoffeeMachine
  Faucet, WineBottle_0, SoapBottle are in/on Sink"""  
  ...
120: 2023/04/26 15:09:41 - 15:10:10: """Goal: Place(DiningTable)
  Visual observation: Tomato_1_Sliced_2, Tomato_1_Sliced_1, Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Bowl_2, WineBottle_2 [filled], Kettle_1, Bread_1, Book_0, DiningTable, Plate, Spatula, Spoon, HousePlant, Chair_1, Chair_2, CounterTop_0, Tomato_1_Sliced_0, Potato_1, Floor, Fork, agent hand, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Chair_2, Chair_1, DiningTable are in/on Floor
  ButterKnife, Fork, Potato_1, Tomato_1_Sliced_0 are in/on CounterTop_0
  Lettuce_Sliced_4, Lettuce_Sliced_5, Spatula, Lettuce_Sliced_3, Bread_1, HousePlant, Lettuce_Sliced_6, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Lettuce_Sliced_0, Bowl_2, WineBottle_2, Kettle_1, Lettuce_Sliced_2, Lettuce_Sliced_1 are in/on DiningTable
  Mug is in/on CoffeeMachine
  Plate is inside agent hand"""  
  ...
...
129: 2023/04/26 15:12:16 - 15:12:47: """Goal: Pickup(Potato_0)
  Visual observation: Potato_1, Sink, StoveBurner_0, CounterTop_0, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, StoveBurner_3, Fork, Window_0, WineBottle_0 [filled], Potato_0, Sink_Basin, SaltShaker, DishSponge, Apple, Pan_0 [dirty], CoffeeMachine [toggled], SoapBottle, Faucet [toggled], Plate, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, Lettuce_Sliced_1, DiningTable, ButterKnife, Mug [filled]
  Potato_0, ButterKnife, DishSponge, Potato_1, Sink, Tomato_1_Sliced_0, Fork, Apple, CoffeeMachine are in/on CounterTop_0
  Tomato_1_Sliced_2, Tomato_1_Sliced_1, Lettuce_Sliced_1 are in/on Plate
  WineBottle_0, Faucet, SoapBottle are in/on Sink
  Tomato_1_Sliced_1, Lettuce_Sliced_1, Tomato_1_Sliced_2, Plate are in/on DiningTable
  Mug is in/on CoffeeMachine
  Speech:
  2023-04-26 15:12:16.187522: The potato you took out of the sink"""  
  ...
130: 2023/04/26 15:12:57 - 15:13:04: """Goal: Place(CounterTop_0)
  Visual observation: Tomato_1_Sliced_0, Pan_1 [dirty], Cabinet_0, CounterTop_0, Cabinet_3, Drawer_0, Potato_0, Pot [dirty], ButterKnife, Plate, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Lettuce_Sliced_1, Potato_1, DiningTable, Fork, agent hand, CoffeeMachine [toggled], Mug [filled]
  Tomato_1_Sliced_0, Potato_1, Pot, ButterKnife, Pan_1, Fork are in/on CounterTop_0
  Tomato_1_Sliced_1, Lettuce_Sliced_1, Plate, Tomato_1_Sliced_2 are in/on DiningTable
  Tomato_1_Sliced_1, Lettuce_Sliced_1, Tomato_1_Sliced_2 are in/on Plate
  Potato_0 is inside agent hand
  Mug is in/on CoffeeMachine"""  
  ...
...
135: 2023/04/26 15:13:38 - 15:13:51: """Goal: Place(Sink_Basin)
  Visual observation: Pan_1 [dirty], Potato_1, Sink, StoveBurner_0, CounterTop_0, StoveBurner_1, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, StoveBurner_3, Fork, Window_0, WineBottle_0 [filled], Sink_Basin, SaltShaker, StoveKnob_3 [toggled], DishSponge, Apple, Pan_0 [dirty], CoffeeMachine [toggled], SoapBottle, Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, agent hand, DiningTable, Plate, ButterKnife, Mug [filled]
  Potato_1, Potato_0_Sliced_7, Potato_0_Sliced_1, Sink, Potato_0_Sliced_5, CoffeeMachine, Potato_0_Sliced_2, ButterKnife, Apple, Potato_0_Sliced_0, Potato_0_Sliced_4, Potato_0_Sliced_3, Fork, DishSponge, Potato_0_Sliced_6 are in/on CounterTop_0
  WineBottle_0, SoapBottle, Faucet are in/on Sink
  Mug is in/on CoffeeMachine
  Plate is in/on DiningTable
  Pan_1 is inside agent hand"""  
  ...
136: 2023/04/26 15:13:55 - 15:13:55: """Goal: ToggleOn(Faucet)
  Visual observation: Pan_1 [dirty], Potato_1, Sink, StoveBurner_0, CounterTop_0, StoveBurner_1, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, StoveBurner_3, Fork, Window_0, WineBottle_0 [filled], Sink_Basin, SaltShaker, StoveKnob_3 [toggled], DishSponge, Apple, Pan_0 [dirty], CoffeeMachine [toggled], SoapBottle, Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, DiningTable, Plate, ButterKnife, Mug [filled]
  Potato_1, Potato_0_Sliced_7, Potato_0_Sliced_1, Sink, Potato_0_Sliced_5, CoffeeMachine, Potato_0_Sliced_2, Apple, Potato_0_Sliced_0, Potato_0_Sliced_4, Potato_0_Sliced_3, ButterKnife, Fork, DishSponge, Potato_0_Sliced_6 are in/on CounterTop_0
  WineBottle_0, SoapBottle, Faucet are in/on Sink
  Plate is in/on DiningTable
  Mug is in/on CoffeeMachine
  Pan_1 is in/on Sink_Basin"""  
  ...
137: 2023/04/26 15:14:00 - 15:14:00: """Goal: ToggleOff(Faucet)
  Visual observation: Pan_1, Potato_1, Sink, StoveBurner_0, CounterTop_0, StoveBurner_1, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, StoveBurner_3, Fork, Window_0, WineBottle_0 [filled], Sink_Basin, SaltShaker, StoveKnob_3 [toggled], DishSponge, Apple, Pan_0 [dirty], CoffeeMachine [toggled], SoapBottle, Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, DiningTable, Plate, ButterKnife, Mug [filled]
  Potato_1, Potato_0_Sliced_7, Potato_0_Sliced_1, Sink, Potato_0_Sliced_5, CoffeeMachine, Potato_0_Sliced_2, Apple, Potato_0_Sliced_0, Potato_0_Sliced_4, Potato_0_Sliced_3, ButterKnife, Fork, DishSponge, Potato_0_Sliced_6 are in/on CounterTop_0
  WineBottle_0, SoapBottle, Faucet are in/on Sink
  Plate is in/on DiningTable
  Mug is in/on CoffeeMachine
  Pan_1 is in/on Sink_Basin"""  
  ...
138: 2023/04/26 15:14:03 - 15:14:03: """Goal: Pickup(Pan_1)
  Visual observation: Pan_1, Potato_1, Sink, StoveBurner_0, CounterTop_0, StoveBurner_1, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, StoveBurner_3, Fork, Window_0, WineBottle_0 [filled], Sink_Basin, SaltShaker, StoveKnob_3 [toggled], DishSponge, Apple, Pan_0 [dirty], CoffeeMachine [toggled], SoapBottle, Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, DiningTable, Plate, ButterKnife, Mug [filled]
  Potato_1, Potato_0_Sliced_7, Potato_0_Sliced_1, Sink, Potato_0_Sliced_5, CoffeeMachine, Potato_0_Sliced_2, Apple, Potato_0_Sliced_0, Potato_0_Sliced_4, Potato_0_Sliced_3, ButterKnife, Fork, DishSponge, Potato_0_Sliced_6 are in/on CounterTop_0
  WineBottle_0, SoapBottle, Faucet are in/on Sink
  Plate is in/on DiningTable
  Mug is in/on CoffeeMachine
  Pan_1 is in/on Sink_Basin"""  
  ...
139: 2023/04/26 15:14:05 - 15:14:11: """Goal: Place(StoveBurner_3)
  Visual observation: Pan_1, Sink, StoveBurner_0, CounterTop_0, StoveBurner_1, Cabinet_4, Cabinet_5, Cabinet_6, Cabinet_8, Cabinet_9, Drawer_1, Drawer_2, StoveBurner_3, CounterTop_1, Microwave [toggled], SaltShaker, Toaster, Pan_0 [dirty], Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, agent hand, Potato_1, Fork, DiningTable, Plate, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Potato_0_Sliced_0, Potato_0_Sliced_2, Potato_0_Sliced_5, Sink, Potato_1, ButterKnife, Potato_0_Sliced_1, Potato_0_Sliced_4, Potato_0_Sliced_7, Potato_0_Sliced_3, Potato_0_Sliced_6, Fork are in/on CounterTop_0
  Plate is in/on DiningTable
  Pan_1 is inside agent hand
  Mug is in/on CoffeeMachine"""  
  ...
140: 2023/04/26 15:14:13 - 15:14:23: """Goal: Pickup(Potato_0_Sliced_5)
  Visual observation: Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Tomato_1_Sliced_0, Cabinet_0, CounterTop_0, Cabinet_3, Drawer_0, Pot [dirty], StoveBurner_3, Pan_1, Potato_1, Fork, DiningTable, Plate, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Potato_0_Sliced_0, Potato_1, Potato_0_Sliced_6, Potato_0_Sliced_7, Pot, Potato_0_Sliced_2, ButterKnife, Fork, Potato_0_Sliced_3, Tomato_1_Sliced_0, Potato_0_Sliced_5, Potato_0_Sliced_1, Potato_0_Sliced_4 are in/on CounterTop_0
  Plate is in/on DiningTable
  Pan_1 is in/on StoveBurner_3
  Mug is in/on CoffeeMachine"""  
  ...
141: 2023/04/26 15:14:25 - 15:14:42: """Goal: Place(Pan_1)
  Visual observation: Potato_0_Sliced_5, Pan_1, Sink, StoveBurner_0, CounterTop_0, StoveBurner_1, StoveBurner_2, Cabinet_4, Cabinet_5, Cabinet_6, Cabinet_8, Cabinet_9, Drawer_1, Drawer_2, CounterTop_1, Microwave [toggled], SaltShaker, StoveKnob_0, StoveKnob_2 [toggled], StoveKnob_3 [toggled], Toaster, Pan_0 [dirty], Potato_0_Sliced_7, Potato_0_Sliced_6, agent hand, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Potato_1, Fork, DiningTable, Plate, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Mug is in/on CoffeeMachine
  Potato_0_Sliced_2, Sink, Potato_0_Sliced_6, Potato_0_Sliced_7, ButterKnife, Potato_1, Potato_0_Sliced_1, Potato_0_Sliced_3, Fork, Potato_0_Sliced_4, Potato_0_Sliced_0 are in/on CounterTop_0
  Potato_0_Sliced_5 is inside agent hand
  Plate is in/on DiningTable
  Pan_1 is in/on StoveBurner_3"""  
  ...
...
145: 2023/04/26 15:15:02 - 15:15:10: """Goal: Pickup(Potato_0_Sliced_5)
  Visual observation: Potato_0_Sliced_5 [cooked], Pan_1, Sink, CounterTop_0, StoveBurner_1, StoveBurner_2, Cabinet_4, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, Microwave [toggled], Window_0, WineBottle_0 [filled], SaltShaker, StoveKnob_0 [toggled], StoveKnob_1 [toggled], StoveKnob_2 [toggled], StoveKnob_3 [toggled], Toaster, Pan_0 [dirty], SoapBottle, Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Potato_1, Fork, DiningTable, Plate, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Mug is in/on CoffeeMachine
  Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_1, Potato_0_Sliced_1, Potato_0_Sliced_0, Potato_0_Sliced_3, Potato_0_Sliced_7, ButterKnife, Sink, Fork, Potato_0_Sliced_6, Potato_0_Sliced_2 are in/on CounterTop_0
  Pan_1 is in/on StoveBurner_3
  WineBottle_0, Faucet, SoapBottle are in/on Sink
  Plate is in/on DiningTable"""  
  ...
146: 2023/04/26 15:15:12 - 15:15:42: """Goal: Place(Plate)
  Visual observation: Potato_0_Sliced_5 [cooked], Tomato_1_Sliced_2, Tomato_1_Sliced_1, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Bowl_2, WineBottle_2 [filled], Kettle_1, Bread_1, Book_0, DiningTable, Plate, Spatula, Spoon, HousePlant, Chair_1, Chair_2, CounterTop_0, Potato_0_Sliced_7, Potato_0_Sliced_6, agent hand, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Pan_1, Potato_1, Floor, Fork, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Potato_0_Sliced_2, Potato_0_Sliced_1, Fork, Potato_0_Sliced_4, Potato_1, Potato_0_Sliced_3, Potato_0_Sliced_6, Potato_0_Sliced_7, ButterKnife, Potato_0_Sliced_0 are in/on CounterTop_0
  Chair_2, Chair_1, DiningTable are in/on Floor
  Lettuce_Sliced_4, Plate, Lettuce_Sliced_5, Spatula, Lettuce_Sliced_3, Bread_1, HousePlant, Tomato_1_Sliced_1, Tomato_1_Sliced_2, Lettuce_Sliced_0, Bowl_2, WineBottle_2, Kettle_1, Lettuce_Sliced_2, Lettuce_Sliced_1 are in/on DiningTable
  Lettuce_Sliced_1, Tomato_1_Sliced_2, Tomato_1_Sliced_1 are in/on Plate
  Mug is in/on CoffeeMachine
  Potato_0_Sliced_5 is inside agent hand
  Pan_1 is in/on StoveBurner_3"""  
  ...
...
148: 2023/04/26 15:16:12 - 15:16:25: """Goal: Place(Pan_1)
  Visual observation: Potato_0_Sliced_3, Pan_1, Sink, CounterTop_0, StoveBurner_1, StoveBurner_2, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, Microwave [toggled], Window_0, WineBottle_0 [filled], Sink_Basin, SaltShaker, StoveKnob_0 [toggled], StoveKnob_1 [toggled], StoveKnob_3 [toggled], Toaster, DishSponge, Pan_0 [dirty], SoapBottle, Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Plate, Potato_0_Sliced_5 [cooked], Potato_0_Sliced_4, agent hand, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Potato_1, DiningTable, Fork, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Plate, Potato_0_Sliced_5 are in/on DiningTable
  SoapBottle, Faucet, WineBottle_0 are in/on Sink
  Potato_0_Sliced_4, Potato_0_Sliced_2, Potato_1, Potato_0_Sliced_7, Sink, Fork, ButterKnife, Potato_0_Sliced_6, Potato_0_Sliced_0, DishSponge, Potato_0_Sliced_1 are in/on CounterTop_0
  Mug is in/on CoffeeMachine
  Potato_0_Sliced_3 is inside agent hand
  Potato_0_Sliced_5 is in/on Plate
  Pan_1 is in/on StoveBurner_3"""  
  ...
149: 2023/04/26 15:16:32 - 15:16:32: """Goal: Pickup(Potato_0_Sliced_3)
  Visual observation: Potato_0_Sliced_3 [cooked], Pan_1, Sink, CounterTop_0, StoveBurner_1, StoveBurner_2, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_9, Drawer_2, Microwave [toggled], Window_0, WineBottle_0 [filled], Sink_Basin, SaltShaker, StoveKnob_0 [toggled], StoveKnob_1 [toggled], StoveKnob_3 [toggled], Toaster, DishSponge, Pan_0 [dirty], SoapBottle, Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Plate, Potato_0_Sliced_5 [cooked], Potato_0_Sliced_4, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Potato_1, DiningTable, Fork, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Potato_0_Sliced_3, Pan_1 are in/on StoveBurner_3
  Potato_0_Sliced_5, Plate are in/on DiningTable
  SoapBottle, Faucet, WineBottle_0 are in/on Sink
  Potato_0_Sliced_3 is in/on Pan_1
  Potato_0_Sliced_4, Potato_0_Sliced_1, Potato_0_Sliced_7, ButterKnife, Sink, Potato_0_Sliced_6, DishSponge, Potato_1, Fork, Potato_0_Sliced_2, Potato_0_Sliced_0 are in/on CounterTop_0
  Mug is in/on CoffeeMachine
  Potato_0_Sliced_5 is in/on Plate"""  
  ...
150: 2023/04/26 15:16:34 - 15:16:58: """Goal: Place(Plate)
  Visual observation: Potato_0_Sliced_5 [cooked], Potato_0_Sliced_3 [cooked], Tomato_1_Sliced_2, Tomato_1_Sliced_1, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Bowl_2, WineBottle_2 [filled], Kettle_1, Bowl_1 [dirty], Bread_1, Book_0, DiningTable, Plate, Spatula, PepperShaker_0, Spoon, HousePlant, Chair_1, Chair_2, CounterTop_0, Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_4, agent hand, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Pan_1, Potato_1, Floor, Fork, ButterKnife, CoffeeMachine [toggled], Mug [filled]
  Plate, Lettuce_Sliced_2, PepperShaker_0, Bowl_1, Tomato_1_Sliced_1, Lettuce_Sliced_5, Lettuce_Sliced_4, Spatula, Potato_0_Sliced_5, Kettle_1, Lettuce_Sliced_3, Bread_1, Tomato_1_Sliced_2, Lettuce_Sliced_0, Bowl_2, Lettuce_Sliced_1, HousePlant, WineBottle_2 are in/on DiningTable
  Potato_0_Sliced_6, Potato_0_Sliced_2, Potato_0_Sliced_0, Potato_0_Sliced_4, ButterKnife, Potato_0_Sliced_1, Potato_1, Fork, Potato_0_Sliced_7 are in/on CounterTop_0
  Tomato_1_Sliced_2, Lettuce_Sliced_1, Tomato_1_Sliced_1, Potato_0_Sliced_5 are in/on Plate
  Chair_1, Chair_2, DiningTable are in/on Floor
  Mug is in/on CoffeeMachine
  Pan_1 is in/on StoveBurner_3
  Potato_0_Sliced_3 is inside agent hand"""  
  ...
151: 2023/04/26 15:17:05 - 15:18:08: """Goal: Pickup(Mug)
  Visual observation: Potato_1, Sink, CounterTop_0, Cabinet_3, Cabinet_6, Cabinet_7, Cabinet_10, Cabinet_11, Fork, Window_0, WineBottle_0 [filled], Sink_Basin, DishSponge, Apple, CoffeeMachine [toggled], Mug [filled], Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Plate, Potato_0_Sliced_5 [cooked], Potato_0_Sliced_4, Potato_0_Sliced_3 [cooked], Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Pan_1, DiningTable, ButterKnife
  CoffeeMachine, Fork, Potato_0_Sliced_4, Potato_0_Sliced_7, Potato_0_Sliced_2, ButterKnife, Apple, Mug, Potato_1, Potato_0_Sliced_6, Potato_0_Sliced_1, DishSponge, Potato_0_Sliced_0, Sink are in/on CounterTop_0
  Faucet, WineBottle_0 are in/on Sink
  Mug is in/on CoffeeMachine
  Potato_0_Sliced_5, Potato_0_Sliced_3 are in/on Plate
  Potato_0_Sliced_5, Potato_0_Sliced_3, Plate are in/on DiningTable
  Pan_1 is in/on StoveBurner_3
  Speech:
  2023-04-26 15:17:28.497944: the coffee you made needs to be on the dining table"""  
  ...
152: 2023/04/26 15:18:14 - 15:18:21: """Goal: Place(CoffeeMachine)
  Visual observation: Potato_1, Sink, CounterTop_0, Cabinet_3, Cabinet_6, Cabinet_7, Cabinet_10, Cabinet_11, Fork, Window_0, WineBottle_0 [filled], Sink_Basin, DishSponge, CoffeeMachine [toggled], Mug [filled], Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Plate, Potato_0_Sliced_5 [cooked], Potato_0_Sliced_4, Potato_0_Sliced_3 [cooked], Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Pan_1, DiningTable, ButterKnife, agent hand
  Potato_0_Sliced_5, Plate, Potato_0_Sliced_3 are in/on DiningTable
  Potato_0_Sliced_4, Fork, Potato_0_Sliced_2, Potato_0_Sliced_6, Potato_0_Sliced_1, CoffeeMachine, Potato_0_Sliced_7, ButterKnife, Potato_1, Potato_0_Sliced_0, DishSponge, Sink are in/on CounterTop_0
  Potato_0_Sliced_5, Potato_0_Sliced_3 are in/on Plate
  Mug is inside agent hand
  WineBottle_0, Faucet are in/on Sink
  Pan_1 is in/on StoveBurner_3"""  
  ...
153: 2023/04/26 15:18:37 - 15:18:37: """Goal: Pickup(Mug)
  Visual observation: Potato_1, Sink, CounterTop_0, Cabinet_3, Cabinet_6, Cabinet_7, Cabinet_10, Cabinet_11, Fork, Window_0, WineBottle_0 [filled], Sink_Basin, DishSponge, Apple, CoffeeMachine [toggled], Mug [filled], Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Plate, Potato_0_Sliced_5 [cooked], Potato_0_Sliced_4, Potato_0_Sliced_3 [cooked], Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Pan_1, DiningTable, ButterKnife
  CoffeeMachine, Fork, Potato_0_Sliced_4, Potato_0_Sliced_7, Potato_0_Sliced_2, ButterKnife, Apple, Mug, Potato_1, Potato_0_Sliced_6, Potato_0_Sliced_1, DishSponge, Potato_0_Sliced_0, Sink are in/on CounterTop_0
  Faucet, WineBottle_0 are in/on Sink
  Mug is in/on CoffeeMachine
  Potato_0_Sliced_5, Potato_0_Sliced_3 are in/on Plate
  Potato_0_Sliced_5, Potato_0_Sliced_3, Plate are in/on DiningTable
  Pan_1 is in/on StoveBurner_3"""  
  ...
154: 2023/04/26 15:18:40 - 15:19:07: """Goal: Place(DiningTable)
  Visual observation: Potato_0_Sliced_5 [cooked], Potato_0_Sliced_3 [cooked], Tomato_1_Sliced_2, Tomato_1_Sliced_1, Lettuce_Sliced_0, Bowl_2, WineBottle_2 [filled], Kettle_1, Bread_1, DiningTable, Plate, Spatula, HousePlant, Mug [filled], Chair_1, CounterTop_0, Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_4, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Pan_1, Potato_1, Floor, Fork, ButterKnife, agent hand
  Potato_0_Sliced_5, Tomato_1_Sliced_2, Potato_0_Sliced_3, Tomato_1_Sliced_1 are in/on Plate
  Pan_1 is in/on StoveBurner_3
  Potato_0_Sliced_1, Fork, Potato_0_Sliced_0, Potato_0_Sliced_6, Potato_0_Sliced_2, ButterKnife, Potato_0_Sliced_4, Potato_0_Sliced_7, Potato_1 are in/on CounterTop_0
  Spatula, WineBottle_2, Kettle_1, Tomato_1_Sliced_1, Lettuce_Sliced_0, Bowl_2, HousePlant, Potato_0_Sliced_5, Potato_0_Sliced_3, Tomato_1_Sliced_2, Bread_1, Plate are in/on DiningTable
  DiningTable, Chair_1 are in/on Floor
  Mug is inside agent hand"""  
  ...
155: 2023/04/26 15:19:10 - 15:19:38: """Goal: Pickup(Potato_1)
  Visual observation: Potato_1, Sink, CounterTop_0, Cabinet_5, Cabinet_6, Cabinet_7, Cabinet_10, Fork, Window_0, WineBottle_0 [filled], Sink_Basin, DishSponge, Apple, CoffeeMachine [toggled], SoapBottle, Faucet [toggled], Potato_0_Sliced_7, Potato_0_Sliced_6, Plate, Potato_0_Sliced_5 [cooked], Potato_0_Sliced_4, Potato_0_Sliced_3 [cooked], Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, StoveBurner_3, Pan_1, DiningTable, ButterKnife, Mug [filled]
  Mug, Potato_0_Sliced_5, Plate, Potato_0_Sliced_3 are in/on DiningTable
  Potato_0_Sliced_4, DishSponge, Potato_0_Sliced_2, Potato_0_Sliced_6, Potato_0_Sliced_1, Fork, CoffeeMachine, Potato_0_Sliced_7, ButterKnife, Potato_1, Potato_0_Sliced_0, Apple, Sink are in/on CounterTop_0
  Potato_0_Sliced_5, Potato_0_Sliced_3 are in/on Plate
  SoapBottle, WineBottle_0, Faucet are in/on Sink
  Pan_1 is in/on StoveBurner_3
  Speech:
  2023-04-26 15:19:15.951067: The potato is still next to the sink."""  
  ...
156: 2023/04/26 15:19:41 - 15:19:48: """Goal: Place(CounterTop_0)
  Visual observation: Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_4, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Tomato_1_Sliced_0, Potato_1, Cabinet_0, CounterTop_0, Cabinet_3, Drawer_0, Pot [dirty], Plate, Potato_0_Sliced_5 [cooked], Potato_0_Sliced_3 [cooked], StoveBurner_3, Pan_1, agent hand, DiningTable, Fork, ButterKnife, Mug [filled]
  Potato_0_Sliced_1, Potato_0_Sliced_6, Fork, Potato_0_Sliced_0, Potato_0_Sliced_4, Potato_0_Sliced_7, Pot, ButterKnife, Tomato_1_Sliced_0, Potato_0_Sliced_2 are in/on CounterTop_0
  Pan_1 is in/on StoveBurner_3
  Plate, Potato_0_Sliced_5, Potato_0_Sliced_3, Mug are in/on DiningTable
  Potato_0_Sliced_3, Potato_0_Sliced_5 are in/on Plate
  Potato_1 is inside agent hand"""  
  ...
...
162: 2023/04/27 09:53:11 - 09:53:17: """Goal: Place(CounterTop)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine [toggled], Faucet [toggled], CounterTop, Floor, agent hand, Mug_0
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Tomato_0, Toaster are in/on CounterTop
  Mug_0 is inside agent hand
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
163: 2023/04/27 09:53:19 - 09:53:19: """Goal: Pickup(Mug_1)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine [toggled], Faucet [toggled], CounterTop, Floor, Mug_0
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Mug_0, Tomato_0, Toaster are in/on CounterTop
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
164: 2023/04/27 09:53:22 - 09:53:22: """Goal: Place(CounterTop)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine [toggled], Faucet [toggled], agent hand, CounterTop, Floor, Mug_0
  Spatula_0, Knife_0, Toaster, Mug_0, Tomato_0, CoffeeMachine are in/on CounterTop
  Cabinet_10, Cabinet_8, Cabinet_9, Cabinet_7 are in/on Floor
  Mug_1 is inside agent hand"""  
  ...
165: 2023/04/27 09:53:25 - 09:53:25: """Goal: Pickup(Mug_0)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine [toggled], Faucet [toggled], CounterTop, Floor, Mug_0
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Mug_0, Tomato_0, Toaster are in/on CounterTop
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
166: 2023/04/27 09:53:29 - 09:53:29: """Goal: Place(CoffeeMachine)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine [toggled], Faucet [toggled], CounterTop, Floor, agent hand, Mug_0
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Tomato_0, Toaster are in/on CounterTop
  Mug_0 is inside agent hand
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
167: 2023/04/27 09:53:32 - 09:53:36: """Goal: ToggleOff(CoffeeMachine)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine [toggled], Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Tomato_0, Toaster are in/on CounterTop
  Mug_0 is in/on CoffeeMachine
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
168: 2023/04/27 09:53:39 - 09:53:39: """Goal: ToggleOn(CoffeeMachine)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Tomato_0, Toaster are in/on CounterTop
  Mug_0 is in/on CoffeeMachine
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
169: 2023/04/27 09:53:47 - 09:53:54: """Goal: ToggleOff(CoffeeMachine)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Tomato_0, Toaster are in/on CounterTop
  Mug_0 is in/on CoffeeMachine
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
170: 2023/04/27 09:53:59 - 09:53:59: """Goal: ToggleOn(CoffeeMachine)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Tomato_0, Toaster are in/on CounterTop
  Mug_0 is in/on CoffeeMachine
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
171: 2023/04/27 09:54:04 - 09:54:07: """Goal: Pickup(Mug_0)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Tomato_0, Toaster are in/on CounterTop
  Mug_0 is in/on CoffeeMachine
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
172: 2023/04/27 09:54:10 - 09:54:10: """Goal: Place(CounterTop)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, agent hand, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Tomato_0, Toaster are in/on CounterTop
  Mug_0 is inside agent hand
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
173: 2023/04/27 09:54:12 - 09:54:12: """Goal: Pickup(Mug_1)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Mug_0, Tomato_0, Toaster are in/on CounterTop
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
174: 2023/04/27 09:54:15 - 09:54:19: """Goal: Pour(Sink)
  Visual observation: Mug_1 [dirty, filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], agent hand, CounterTop, Floor, Mug_0 [filled]
  Spatula_0, Knife_0, Toaster, Mug_0, Tomato_0, CoffeeMachine are in/on CounterTop
  Cabinet_10, Cabinet_8, Cabinet_9, Cabinet_7 are in/on Floor
  Mug_1 is inside agent hand"""  
  ...
175: 2023/04/27 09:54:25 - 09:54:25: """Goal: Place(CoffeeMachine)
  Visual observation: Mug_1 [dirty], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], agent hand, CounterTop, Floor, Mug_0 [filled]
  Spatula_0, Knife_0, Toaster, Mug_0, Tomato_0, CoffeeMachine are in/on CounterTop
  Cabinet_10, Cabinet_8, Cabinet_9, Cabinet_7 are in/on Floor
  Mug_1 is inside agent hand"""  
  ...
176: 2023/04/27 09:54:28 - 09:54:28: """Goal: ToggleOff(CoffeeMachine)
  Visual observation: Mug_1 [dirty], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Mug_0, Tomato_0, Toaster are in/on CounterTop
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor
  Mug_1 is in/on CoffeeMachine"""  
  ...
177: 2023/04/27 09:54:32 - 09:54:32: """Goal: ToggleOn(CoffeeMachine)
  Visual observation: Mug_1 [dirty], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Mug_0, Tomato_0, Toaster are in/on CounterTop
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor
  Mug_1 is in/on CoffeeMachine"""  
  ...
178: 2023/04/27 09:54:45 - 09:54:53: """Goal: ToggleOff(Faucet)
  Visual observation: Mug_1 [dirty], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet [toggled], CounterTop, Floor, Mug_0 [filled]
  Mug_1, Spatula_0, Knife_0, CoffeeMachine, Mug_0, Tomato_0, Toaster are in/on CounterTop
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor
  Mug_1 is in/on CoffeeMachine"""  
  ...
...
181: 2023/04/27 09:55:03 - 09:55:03: """Goal: ToggleOn(Faucet)
  Visual observation: Mug_1 [dirty], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet, CounterTop, Floor, Mug_0 [filled]
  Spatula_0, Knife_0, CoffeeMachine, Mug_0, Tomato_0, Toaster are in/on CounterTop
  Mug_1, Knife_1 are in/on Sink_Basin
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
182: 2023/04/27 09:55:07 - 09:55:07: """Goal: ToggleOff(Faucet)
  Visual observation: Mug_1 [filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet, CounterTop, Floor, Mug_0 [filled]
  Spatula_0, Knife_0, CoffeeMachine, Mug_0, Tomato_0, Toaster are in/on CounterTop
  Mug_1, Knife_1 are in/on Sink_Basin
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor"""  
  ...
...
189: 2023/04/27 09:56:59 - 09:57:11: """Goal: Open(Cabinet_9)
  Visual observation: Mug_1 [filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_11, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet, CounterTop, Floor, agent hand, Mug_0 [filled]
  Mug_1, Toaster, Spatula_0, CoffeeMachine, Tomato_0, Mug_0 are in/on CounterTop
  Cabinet_10, Cabinet_8, Cabinet_9, Cabinet_7 are in/on Floor
  Knife_0 is inside agent hand
  Mug_1 is in/on CoffeeMachine
  Speech:
  2023-04-27 09:56:59.224832: and lettuce is in the cupboard under and left of the sink"""  
  ...
190: 2023/04/27 09:57:15 - 09:57:15: """Goal: Open(Cabinet_10)
  Visual observation: Mug_1 [filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9 [open], Cabinet_10, Cabinet_11, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet, CounterTop, Floor, agent hand, Mug_0 [filled]
  Mug_1, Toaster, Spatula_0, CoffeeMachine, Tomato_0, Mug_0 are in/on CounterTop
  Cabinet_10, Cabinet_8, Cabinet_9, Cabinet_7 are in/on Floor
  Knife_0 is inside agent hand
  Mug_1 is in/on CoffeeMachine"""  
  ...
191: 2023/04/27 09:57:18 - 09:57:18: """Goal: Open(Cabinet_8)
  Visual observation: Mug_1 [filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8, Cabinet_9 [open], Cabinet_10 [open], Cabinet_11, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet, CounterTop, Floor, agent hand, Mug_0 [filled]
  Mug_1, Toaster, Spatula_0, CoffeeMachine, Tomato_0, Mug_0 are in/on CounterTop
  Cabinet_10, Cabinet_8, Cabinet_9, Cabinet_7 are in/on Floor
  Knife_0 is inside agent hand
  Mug_1 is in/on CoffeeMachine"""  
  ...
192: 2023/04/27 09:57:22 - 09:57:22: """Goal: Slice(Lettuce)
  Visual observation: Mug_1 [filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8 [open], Cabinet_9 [open], Cabinet_10 [open], Cabinet_11, Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Lettuce, Faucet, CounterTop, Floor, agent hand, Mug_0 [filled]
  Cabinet_10, Cabinet_8, Cabinet_9, Cabinet_7 are in/on Floor
  Mug_1, Toaster, CoffeeMachine, Mug_0, Spatula_0, Tomato_0 are in/on CounterTop
  Knife_0 is inside agent hand
  Mug_1 is in/on CoffeeMachine"""  
  ...
...
199: 2023/04/27 09:58:06 - 09:58:09: """Goal: Open(Cabinet_2)
  Visual observation: Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Knife_1, Cup_1, Sink, Drawer_3, Cabinet_1, Cabinet_2, Cabinet_7, Cabinet_8 [open], Cabinet_9 [open], Window, Spatula_0, Knife_0, Sink_Basin, Faucet, CounterTop, CoffeeMachine, Mug_1 [filled], Floor, Mug_0 [filled]
  Lettuce_Sliced_5, Lettuce_Sliced_2, Lettuce_Sliced_4, Lettuce_Sliced_0, Lettuce_Sliced_3, Lettuce_Sliced_6 are in/on Cabinet_8
  Cabinet_7, Cabinet_9, Cabinet_8 are in/on Floor
  Mug_1, Lettuce_Sliced_1, Knife_0, CoffeeMachine, Cup_1, Mug_0, Spatula_0 are in/on CounterTop
  Mug_1 is in/on CoffeeMachine"""  
  ...
200: 2023/04/27 09:58:11 - 09:58:28: """Goal: Open(Fridge)
  Visual observation: Drawer_4, Cabinet_3 [open], Cabinet_6, Fridge [open], Microwave [toggled], DishSponge_0, CounterTop, Lettuce_Sliced_1, CoffeeMachine, Mug_1 [filled], Floor, Knife_0, Mug_0 [filled]
  Mug_1 is in/on CoffeeMachine
  Lettuce_Sliced_1, Knife_0, Microwave, CoffeeMachine, Mug_0, Mug_1 are in/on CounterTop
  Fridge is in/on Floor"""  
  ...
...
202: 2023/04/27 09:59:04 - 09:59:11: """Goal: Pickup(Knife_0)
  Visual observation: Lettuce_Sliced_3, Lettuce_Sliced_2, Mug_1 [filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8 [open], Cabinet_9 [open], Cabinet_10 [open], Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet, CounterTop, Lettuce_Sliced_1, Floor, Mug_0 [filled]
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor
  Lettuce_Sliced_2, Lettuce_Sliced_3 are in/on Cabinet_8
  Toaster, Mug_0, Knife_0, Lettuce_Sliced_1, Spatula_0, Tomato_0, Mug_1, CoffeeMachine are in/on CounterTop
  Mug_1 is in/on CoffeeMachine"""  
  ...
203: 2023/04/27 09:59:14 - 09:59:14: """Goal: Slice(Tomato_0)
  Visual observation: Lettuce_Sliced_3, Lettuce_Sliced_2, Mug_1 [filled], Knife_1, Sink, Drawer_1, Drawer_2, Drawer_3, Cabinet_7, Cabinet_8 [open], Cabinet_9 [open], Cabinet_10 [open], Tomato_0, Window, Toaster, Spatula_0, Knife_0, Sink_Basin, CoffeeMachine, Faucet, CounterTop, Lettuce_Sliced_1, Floor, agent hand, Mug_0 [filled]
  Cabinet_8, Cabinet_9, Cabinet_10, Cabinet_7 are in/on Floor
  Lettuce_Sliced_2, Lettuce_Sliced_3 are in/on Cabinet_8
  Toaster, Lettuce_Sliced_1, Spatula_0, Tomato_0, Mug_1, Mug_0, CoffeeMachine are in/on CounterTop
  Knife_0 is inside agent hand
  Mug_1 is in/on CoffeeMachine"""  
  ...
204: 2023/04/27 09:59:18 - 09:59:30: """Goal: Open(Fridge)
  Visual observation: Drawer_4, Cabinet_3 [open], Cabinet_6, Fridge [open], Microwave [toggled], Ladle_0, Knife_0, CoffeeMachine, Mug_1 [filled], CounterTop, Floor, agent hand, Mug_0 [filled]
  Microwave, Ladle_0, Mug_1, Mug_0, CoffeeMachine are in/on CounterTop
  Knife_0 is inside agent hand
  Mug_1 is in/on CoffeeMachine
  Fridge is in/on Floor"""  
  ...
...
263: 2023/04/27 10:05:44 - 10:05:44: """Goal: ToggleOn(Faucet)
  Visual observation: Spatula_2, CreditCard_1, Cabinet_0, Window, Sink, CounterTop_2, Knife, Pan, Plate_0 [dirty], PaperTowelRoll, Bowl_0 [dirty, filled], Sink_Basin, DishSponge_0, Faucet, CounterTop_1, Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2 [cooked], Potato_0_Sliced_1, Potato_0_Sliced_0, ButterKnife_2, Kettle_1 [filled], StoveBurner_0
  Plate_0, Pan are in/on Sink_Basin
  Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_4, Kettle_1, Potato_0_Sliced_1, Potato_0_Sliced_0, Potato_0_Sliced_5, ButterKnife_2, Potato_0_Sliced_3 are in/on CounterTop_1
  CounterTop_2, Potato_0_Sliced_2 are in/on Pan
  DishSponge_0, Spatula_2, CreditCard_1, PaperTowelRoll, Bowl_0, Knife are in/on CounterTop_2
  Pan is in/on Plate_0
  Pan is in/on StoveBurner_0"""  
  ...
264: 2023/04/27 10:05:47 - 10:05:47: """Goal: ToggleOff(Faucet)
  Visual observation: Spatula_2, CreditCard_1, Cabinet_0, Window, Sink, CounterTop_2, Knife, Pan, Plate_0, PaperTowelRoll, Bowl_0 [dirty, filled], Sink_Basin, DishSponge_0, Faucet [toggled], CounterTop_1, Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2 [cooked], Potato_0_Sliced_1, Potato_0_Sliced_0, ButterKnife_2, Kettle_1 [filled], StoveBurner_0
  Plate_0, Pan are in/on Sink_Basin
  Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_4, Kettle_1, Potato_0_Sliced_1, Potato_0_Sliced_0, Potato_0_Sliced_5, ButterKnife_2, Potato_0_Sliced_3 are in/on CounterTop_1
  CounterTop_2, Potato_0_Sliced_2 are in/on Pan
  DishSponge_0, Spatula_2, CreditCard_1, PaperTowelRoll, Bowl_0, Knife are in/on CounterTop_2
  Pan is in/on Plate_0
  Pan is in/on StoveBurner_0"""  
  ...
265: 2023/04/27 10:05:50 - 10:05:50: """Goal: Pickup(Plate_0)
  Visual observation: Spatula_2, CreditCard_1, Cabinet_0, Window, Sink, CounterTop_2, Knife, Pan, Plate_0, PaperTowelRoll, Bowl_0 [dirty, filled], Sink_Basin, DishSponge_0, Faucet [toggled], CounterTop_1, Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_2 [cooked], Potato_0_Sliced_1, Potato_0_Sliced_0, ButterKnife_2, Kettle_1 [filled], StoveBurner_0
  Plate_0, Pan are in/on Sink_Basin
  Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_4, Kettle_1, Potato_0_Sliced_1, Potato_0_Sliced_0, Potato_0_Sliced_5, ButterKnife_2, Potato_0_Sliced_3 are in/on CounterTop_1
  CounterTop_2, Potato_0_Sliced_2 are in/on Pan
  DishSponge_0, Spatula_2, CreditCard_1, PaperTowelRoll, Bowl_0, Knife are in/on CounterTop_2
  Pan is in/on Plate_0
  Pan is in/on StoveBurner_0"""  
  ...
266: 2023/04/27 10:05:54 - 10:06:10: """Goal: Place(CounterTop_1)
  Visual observation: Potato_0_Sliced_4, Potato_0_Sliced_3, Potato_0_Sliced_1, Potato_0_Sliced_0, ButterKnife_2, Kettle_1 [filled], Potato_1, Lettuce_1, StoveBurner_0, Drawer_0, StoveBurner_1, CounterTop_1, StoveBurner_2, Drawer_3, Drawer_4, StoveKnob_0, Drawer_5, StoveBurner_3, Cabinet_4, Drawer_7, StoveKnob_3, Cabinet_7, Cabinet_8, Microwave, Pan, Plate_0, ShelvingUnit, Potato_0_Sliced_7, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_2 [cooked], CounterTop_2, Spatula_2, CreditCard_1, Floor, agent hand, PaperTowelRoll, Bowl_0 [dirty, filled]
  CreditCard_1, Bowl_0, PaperTowelRoll, Spatula_2 are in/on CounterTop_2
  Pan is in/on StoveBurner_0
  Potato_0_Sliced_5, Lettuce_1, Potato_1, ButterKnife_2, Potato_0_Sliced_0, Potato_0_Sliced_4, Potato_0_Sliced_7, Kettle_1, Potato_0_Sliced_6, Potato_0_Sliced_3, Potato_0_Sliced_1 are in/on CounterTop_1
  ShelvingUnit is in/on Floor
  Potato_0_Sliced_2 is in/on Pan
  Plate_0 is inside agent hand"""  
  ...
...
275: 2023/04/28 19:50:52 - 19:50:52: """Goal: Pickup(Knife)
  Visual observation: Fork_2, CounterTop_1, Cabinet_0, Cabinet_1, Cabinet_3, Cabinet_4, Cabinet_17, Sink, Drawer_3, Microwave, CoffeeMachine [toggled], Knife, Sink_Basin, ButterKnife, Potato_0, DishSponge, Cup [dirty], Mug [dirty, filled], Faucet, Floor
  CoffeeMachine, Cup, ButterKnife, Faucet, Fork_2 are in/on CounterTop_1
  Mug, DishSponge, Faucet are in/on Sink_Basin
  Cabinet_3, Cabinet_4, Cabinet_17 are in/on Floor
  Potato_0, Knife are in/on Sink"""  
  ...
...
317: 2023/04/28 19:58:46 - 19:58:46: """Goal: Pickup(Lettuce_Sliced_6)
  Visual observation: Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_0, Potato_0_Sliced_8, Potato_0_Sliced_7 [cooked], Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4 [cooked], Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Plate_2, SaltShaker_1, Drawer_1, CounterTop_1, Cabinet_3, Cabinet_17, Sink, GarbageCan, Spatula, CoffeeMachine [toggled], Knife, Sink_Basin, DishSponge, Mug [dirty, filled], Faucet, Lettuce_Sliced_2, Lettuce_Sliced_1, Floor, Cabinet_1 [open], Potato_2, Apple_1
  Lettuce_Sliced_5, Knife, Lettuce_Sliced_4, Apple_1, CoffeeMachine, Spatula, Lettuce_Sliced_2, Lettuce_Sliced_3, Lettuce_Sliced_1, Faucet, Lettuce_Sliced_6 are in/on CounterTop_1
  Potato_0_Sliced_2, Potato_0_Sliced_6, Potato_0_Sliced_0, Potato_0_Sliced_8, Potato_0_Sliced_1, Potato_0_Sliced_3, Potato_0_Sliced_5 are in/on Sink
  Potato_0_Sliced_7, Cabinet_17, Lettuce_Sliced_0, SaltShaker_1, Potato_0_Sliced_4, Cabinet_3, Plate_2, GarbageCan are in/on Floor
  Faucet, Mug, DishSponge are in/on Sink_Basin
  Potato_2 is in/on Cabinet_1
  Potato_0_Sliced_4, Potato_0_Sliced_7 are in/on Plate_2"""  
  ...
318: 2023/04/28 19:58:52 - 19:58:52: """Goal: Place(Floor)
  Visual observation: Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_0, Potato_0_Sliced_8, Potato_0_Sliced_7 [cooked], Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4 [cooked], Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Plate_2, SaltShaker_1, Drawer_1, CounterTop_1, Cabinet_3, Cabinet_17, Sink, GarbageCan, Spatula, CoffeeMachine [toggled], Knife, Sink_Basin, DishSponge, Mug [dirty, filled], Faucet, agent hand, Lettuce_Sliced_2, Lettuce_Sliced_1, Floor, Cabinet_1 [open], Potato_2, Apple_1
  Lettuce_Sliced_5, Knife, Lettuce_Sliced_4, CoffeeMachine, Spatula, Apple_1, Lettuce_Sliced_1, Lettuce_Sliced_3, Lettuce_Sliced_2, Faucet are in/on CounterTop_1
  Potato_0_Sliced_2, Potato_0_Sliced_6, Potato_0_Sliced_0, Potato_0_Sliced_8, Potato_0_Sliced_1, Potato_0_Sliced_3, Potato_0_Sliced_5 are in/on Sink
  SaltShaker_1, Potato_0_Sliced_4, Plate_2, GarbageCan, Cabinet_17, Potato_0_Sliced_7, Lettuce_Sliced_0, Cabinet_3 are in/on Floor
  Faucet, Mug, DishSponge are in/on Sink_Basin
  Lettuce_Sliced_6 is inside agent hand
  Potato_0_Sliced_4, Potato_0_Sliced_7 are in/on Plate_2
  Potato_2 is in/on Cabinet_1"""  
  ...
319: 2023/04/28 19:58:55 - 19:58:55: """Goal: Pickup(Lettuce_Sliced_5)
  Visual observation: Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_0, Potato_0_Sliced_8, Potato_0_Sliced_7 [cooked], Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_4 [cooked], Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Plate_2, SaltShaker_1, Drawer_1, CounterTop_1, Cabinet_3, Cabinet_17, Sink, GarbageCan, Spatula, CoffeeMachine [toggled], Knife, Sink_Basin, DishSponge, Mug [dirty, filled], Faucet, Floor, Lettuce_Sliced_2, Lettuce_Sliced_1, Cabinet_1 [open], Potato_2, Apple_1
  Potato_0_Sliced_7, Cabinet_17, Lettuce_Sliced_0, SaltShaker_1, Cabinet_3, Lettuce_Sliced_6, Plate_2, Potato_0_Sliced_4, GarbageCan are in/on Floor
  Lettuce_Sliced_5, Knife, Lettuce_Sliced_4, Apple_1, CoffeeMachine, Spatula, Lettuce_Sliced_1, Lettuce_Sliced_3, Lettuce_Sliced_2, Faucet are in/on CounterTop_1
  Potato_0_Sliced_2, Potato_0_Sliced_6, Potato_0_Sliced_0, Potato_0_Sliced_8, Potato_0_Sliced_1, Potato_0_Sliced_3, Potato_0_Sliced_5 are in/on Sink
  Faucet, Mug, DishSponge are in/on Sink_Basin
  Potato_2 is in/on Cabinet_1
  Potato_0_Sliced_4, Potato_0_Sliced_7 are in/on Plate_2"""  
  ...
...
325: 2023/04/28 20:00:21 - 20:00:21: """Goal: Place(CounterTop_1)
  Visual observation: Tomato_0_Sliced_6, Tomato_0_Sliced_5, Tomato_0_Sliced_4, Tomato_0_Sliced_3, Tomato_0_Sliced_2, Tomato_0_Sliced_1, Tomato_0_Sliced_0, Lettuce_Sliced_4, Lettuce_Sliced_3, Potato_0_Sliced_8, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Fork_2, Drawer_1, CounterTop_1, Cabinet_3, Cabinet_13, Cabinet_14, Cabinet_17, Sink, Drawer_3, GarbageCan, Microwave [toggled, open], Spatula, CoffeeMachine [toggled], Knife, Sink_Basin, ButterKnife, DishSponge, Mug [dirty, filled], Faucet, Floor, Lettuce_Sliced_6, Plate_2, Lettuce_Sliced_5, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Cabinet_1 [open], Potato_2, SaltShaker_1, Apple_1, Tomato_0, agent hand
  Lettuce_Sliced_6, Plate_2, Cabinet_17, Lettuce_Sliced_0, Cabinet_3, SaltShaker_1, Lettuce_Sliced_5, GarbageCan are in/on Floor
  Apple_1, Lettuce_Sliced_4, Tomato_0_Sliced_0, Tomato_0_Sliced_2, Fork_2, ButterKnife, Tomato_0_Sliced_3, CoffeeMachine, Tomato_0_Sliced_6, Lettuce_Sliced_2, Spatula, Tomato_0_Sliced_1, Lettuce_Sliced_1, Faucet, Tomato_0, Tomato_0_Sliced_4, Tomato_0_Sliced_5, Lettuce_Sliced_3 are in/on CounterTop_1
  Faucet, DishSponge, Mug are in/on Sink_Basin
  Potato_0_Sliced_0, Potato_0_Sliced_3, Potato_0_Sliced_8, Potato_0_Sliced_1, Potato_0_Sliced_5, Potato_0_Sliced_6, Potato_0_Sliced_2 are in/on Sink
  Potato_2 is in/on Cabinet_1
  Lettuce_Sliced_5 is in/on Plate_2
  Knife is inside agent hand"""  
  ...
326: 2023/04/28 20:00:26 - 20:00:26: """Goal: Pickup(Tomato_0_Sliced_4)
  Visual observation: Tomato_0_Sliced_6, Tomato_0_Sliced_5, Tomato_0_Sliced_4, Tomato_0_Sliced_3, Tomato_0_Sliced_2, Tomato_0_Sliced_1, Tomato_0_Sliced_0, Lettuce_Sliced_4, Lettuce_Sliced_3, Potato_0_Sliced_8, Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Fork_2, Drawer_1, CounterTop_1, Cabinet_3, Cabinet_13, Cabinet_14, Cabinet_17, Sink, Drawer_3, GarbageCan, Microwave [toggled, open], Spatula, CoffeeMachine [toggled], Knife, Sink_Basin, ButterKnife, DishSponge, Mug [dirty, filled], Faucet, Floor, Plate_2, Cabinet_1 [open], Potato_2, SaltShaker_1, Apple_1
  Plate_2, Cabinet_17, Cabinet_3, SaltShaker_1, GarbageCan are in/on Floor
  Lettuce_Sliced_4, Tomato_0_Sliced_0, Knife, Tomato_0_Sliced_2, Fork_2, ButterKnife, Tomato_0_Sliced_3, CoffeeMachine, Tomato_0_Sliced_6, Spatula, Tomato_0_Sliced_1, Apple_1, Faucet, Tomato_0_Sliced_4, Tomato_0_Sliced_5, Lettuce_Sliced_3 are in/on CounterTop_1
  Faucet, DishSponge, Mug are in/on Sink_Basin
  Potato_0_Sliced_0, Potato_0_Sliced_3, Potato_0_Sliced_8, Potato_0_Sliced_1, Potato_0_Sliced_5, Potato_0_Sliced_6, Potato_0_Sliced_2 are in/on Sink
  Potato_2 is in/on Cabinet_1"""  
  ...
327: 2023/04/28 20:00:29 - 20:00:32: """Goal: Place(Plate_2)
  Visual observation: Tomato_0_Sliced_6, Tomato_0_Sliced_5, Tomato_0_Sliced_4, Tomato_0_Sliced_3, Tomato_0_Sliced_2, Tomato_0_Sliced_1, Tomato_0_Sliced_0, Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_0, Potato_0_Sliced_8, Potato_0_Sliced_7 [cooked], Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Plate_2, SaltShaker_1, Fork_2, Drawer_1, CounterTop_1, Cabinet_3, Cabinet_4, Cabinet_17, Sink, Drawer_3, GarbageCan, Spatula, CoffeeMachine [toggled], Knife, Sink_Basin, ButterKnife, DishSponge, Mug [dirty, filled], Faucet, agent hand, Floor, Cabinet_1 [open], Potato_2, Apple_1
  Lettuce_Sliced_4, CoffeeMachine, Lettuce_Sliced_3, Knife, Fork_2, ButterKnife, Tomato_0_Sliced_0, Spatula, Tomato_0_Sliced_3, Faucet, Tomato_0_Sliced_2, Apple_1, Tomato_0_Sliced_1, Tomato_0_Sliced_6, Tomato_0_Sliced_5 are in/on CounterTop_1
  Lettuce_Sliced_6, Potato_0_Sliced_7, Cabinet_17, GarbageCan, Cabinet_3, Plate_2, Cabinet_4, Lettuce_Sliced_5, SaltShaker_1, Lettuce_Sliced_0 are in/on Floor
  Faucet, DishSponge, Mug are in/on Sink_Basin
  Potato_0_Sliced_8, Potato_0_Sliced_6, Potato_0_Sliced_2, Potato_0_Sliced_0, Potato_0_Sliced_5, Potato_0_Sliced_1, Potato_0_Sliced_3 are in/on Sink
  Potato_0_Sliced_7, Lettuce_Sliced_5 are in/on Plate_2
  Potato_2 is in/on Cabinet_1
  Tomato_0_Sliced_4 is inside agent hand"""  
  ...
328: 2023/04/28 20:00:36 - 20:00:36: """Goal: Noop
  Visual observation: Tomato_0_Sliced_6, Tomato_0_Sliced_5, Tomato_0_Sliced_4, Tomato_0_Sliced_3, Tomato_0_Sliced_2, Tomato_0_Sliced_1, Tomato_0_Sliced_0, Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_0, Potato_0_Sliced_8, Potato_0_Sliced_7 [cooked], Potato_0_Sliced_6, Potato_0_Sliced_5, Potato_0_Sliced_3, Potato_0_Sliced_2, Potato_0_Sliced_1, Potato_0_Sliced_0, Plate_2, SaltShaker_1, Fork_2, Drawer_1, CounterTop_1, Cabinet_3, Cabinet_4, Cabinet_17, Sink, Drawer_3, GarbageCan, Spatula, CoffeeMachine [toggled], Knife, Sink_Basin, ButterKnife, DishSponge, Mug [dirty, filled], Faucet, Floor, Cabinet_1 [open], Potato_2, Apple_1
  Lettuce_Sliced_4, CoffeeMachine, Lettuce_Sliced_3, Knife, Fork_2, ButterKnife, Apple_1, Tomato_0_Sliced_0, Spatula, Tomato_0_Sliced_3, Faucet, Tomato_0_Sliced_2, Tomato_0_Sliced_1, Tomato_0_Sliced_6, Tomato_0_Sliced_5 are in/on CounterTop_1
  Cabinet_3, Plate_2, Lettuce_Sliced_5, SaltShaker_1, Cabinet_4, Lettuce_Sliced_0, Lettuce_Sliced_6, Potato_0_Sliced_7, GarbageCan, Cabinet_17, Tomato_0_Sliced_4 are in/on Floor
  Faucet, DishSponge, Mug are in/on Sink_Basin
  Potato_0_Sliced_8, Potato_0_Sliced_6, Potato_0_Sliced_2, Potato_0_Sliced_0, Potato_0_Sliced_5, Potato_0_Sliced_1, Potato_0_Sliced_3 are in/on Sink
  Potato_2 is in/on Cabinet_1
  Potato_0_Sliced_7, Tomato_0_Sliced_4, Lettuce_Sliced_5 are in/on Plate_2
  Speech:
  2023-04-28 20:00:36.655591: Great work. Task complete."""  
  ...
...
332: 2023/04/29 11:26:30 - 11:26:51: """Goal: Place(DiningTable)
  Visual observation: Knife_1, DishSponge_1, Pen_1, Spatula_1, Spatula_0, DiningTable, Shelf_0, Chair_1, Shelf_1, Bowl [dirty], agent hand, Floor
  Chair_1, DiningTable, Shelf_0, Spatula_0 are in/on Floor
  DishSponge_1, Bowl, Pen_1, Spatula_1 are in/on DiningTable
  Spatula_0 is in/on Shelf_0
  Knife_1 is inside agent hand
  Speech:
  2023-04-29 11:26:49.818334: Walk a few steps ahead and then look to your right"""  
  ...
...
339: 2023/04/29 11:28:18 - 11:28:27: """Goal: ToggleOff(Toaster)
  Visual observation: Bread_Sliced_4, ButterKnife_1, Pen_2, Cabinet_0, CounterTop, Sink, Cabinet_4, Cabinet_5, Cabinet_9, CoffeeMachine [toggled], Fork, Fridge [open], Pencil, Sink_Basin, Toaster [toggled], Faucet [toggled], DiningTable, Bread_Sliced_5, agent hand, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Knife_1, Floor
  Bread_Sliced_5, Bread_Sliced_2, Bread_Sliced_1, Knife_1, Bread_Sliced_3 are in/on DiningTable
  CoffeeMachine, Toaster, Pen_2, Faucet are in/on CounterTop
  CounterTop, Fork, ButterKnife_1, Pencil are in/on Sink_Basin
  Bread_Sliced_4 is inside agent hand
  Fridge, DiningTable are in/on Floor"""  
  ...
340: 2023/04/29 11:28:30 - 11:28:30: """Goal: Place(Toaster)
  Visual observation: Bread_Sliced_4, ButterKnife_1, Pen_2, Cabinet_0, CounterTop, Sink, Cabinet_4, Cabinet_5, Cabinet_9, CoffeeMachine [toggled], Fork, Fridge [open], Pencil, Sink_Basin, Toaster, Faucet [toggled], DiningTable, Bread_Sliced_5, agent hand, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Knife_1, Floor
  Bread_Sliced_5, Bread_Sliced_2, Bread_Sliced_1, Knife_1, Bread_Sliced_3 are in/on DiningTable
  CoffeeMachine, Toaster, Pen_2, Faucet are in/on CounterTop
  CounterTop, Fork, ButterKnife_1, Pencil are in/on Sink_Basin
  Bread_Sliced_4 is inside agent hand
  Fridge, DiningTable are in/on Floor"""  
  ...
341: 2023/04/29 11:28:31 - 11:28:32: """Goal: ToggleOn(Toaster)
  Visual observation: Bread_Sliced_4, ButterKnife_1, Pen_2, Cabinet_0, CounterTop, Sink, Cabinet_4, Cabinet_5, Cabinet_9, CoffeeMachine [toggled], Fork, Fridge [open], Pencil, Sink_Basin, Toaster, Spoon, Faucet [toggled], DiningTable, Bread_Sliced_5, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Knife_1, Floor
  Faucet, Bread_Sliced_4, CoffeeMachine, Toaster, Pen_2 are in/on CounterTop
  Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_5, Knife_1, Bread_Sliced_1 are in/on DiningTable
  DiningTable, Fridge are in/on Floor
  ButterKnife_1, CounterTop, Spoon, Fork, Pencil are in/on Sink_Basin
  Bread_Sliced_4 is in/on Toaster
  Speech:
  2023-04-29 11:28:31.410192: There is a plate in the fridge to serve the slice on"""  
  ...
342: 2023/04/29 11:28:34 - 11:28:34: """Goal: ToggleOff(Toaster)
  Visual observation: Bread_Sliced_4 [cooked], ButterKnife_1, Pen_2, Cabinet_0, CounterTop, Sink, Cabinet_4, Cabinet_5, Cabinet_9, CoffeeMachine [toggled], Fork, Fridge [open], Pencil, Sink_Basin, Toaster, Spoon, Faucet [toggled], DiningTable, Bread_Sliced_5, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Knife_1, Floor
  Faucet, Bread_Sliced_4, CoffeeMachine, Toaster, Pen_2 are in/on CounterTop
  Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_5, Knife_1, Bread_Sliced_1 are in/on DiningTable
  DiningTable, Fridge are in/on Floor
  ButterKnife_1, CounterTop, Spoon, Fork, Pencil are in/on Sink_Basin
  Bread_Sliced_4 is in/on Toaster"""  
  ...
343: 2023/04/29 11:28:35 - 11:28:42: """Goal: Open(Fridge)
  Visual observation: Cabinet_0, CounterTop, Fridge [open], DiningTable, Bread_Sliced_5, Toaster, Bread_Sliced_4 [cooked], Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Knife_1, Floor, Sink_Basin
  Bread_Sliced_1, Knife_1, Bread_Sliced_3, Bread_Sliced_5, Bread_Sliced_2 are in/on DiningTable
  CounterTop is in/on Sink_Basin
  Toaster, Bread_Sliced_4 are in/on CounterTop
  Fridge, DiningTable are in/on Floor
  Bread_Sliced_4 is in/on Toaster"""  
  ...
...
347: 2023/04/29 11:29:38 - 11:29:48: """Goal: Pickup(Bread_Sliced_4)
  Visual observation: Bread_Sliced_4 [cooked], ButterKnife_1, Cabinet_0, Drawer_0, CounterTop, Sink, Cabinet_3, Cabinet_4, Cabinet_5, Drawer_1, Cabinet_9, CoffeeMachine [toggled], Fork, Pencil, Tomato, Sink_Basin, Toaster, Spoon, Faucet [toggled], DiningTable, Bread_Sliced_5, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Knife_1, Plate_1, Floor
  DiningTable is in/on Floor
  Toaster, Bread_Sliced_4, Tomato, CoffeeMachine, Faucet are in/on CounterTop
  Bread_Sliced_5, Bread_Sliced_1, Knife_1, Bread_Sliced_3, Plate_1, Bread_Sliced_2 are in/on DiningTable
  Pencil, Spoon, CounterTop, ButterKnife_1, Fork are in/on Sink_Basin
  Bread_Sliced_4 is in/on Toaster"""  
  ...
348: 2023/04/29 11:29:49 - 11:30:00: """Goal: Place(Plate_1)
  Visual observation: Bread_Sliced_5, Bread_Sliced_4 [cooked], Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Bread__0, Plate_1, DishSponge_1, Pen_1, DiningTable, Shelf_0, Chair_0, agent hand, Knife_1, Floor
  Bread_Sliced_1, Knife_1, Bread__0, Bread_Sliced_3, Plate_1, Pen_1, Bread_Sliced_5, Bread_Sliced_2, DishSponge_1 are in/on DiningTable
  Chair_0, DiningTable, Shelf_0 are in/on Floor
  Bread_Sliced_4 is inside agent hand"""  
  ...
...
353: 2023/04/29 17:43:09 - 17:43:19: """Goal: ToggleOff(Faucet)
  Visual observation: Drawer_0, Cabinet_0, Cabinet_1, Cabinet_2, Cabinet_3, Cabinet_4, CounterTop_0, Sink, Drawer_1, Drawer_2, Plate_0 [dirty], Apple, Sink_Basin, Microwave [toggled], DishSponge, Faucet [toggled], agent hand, DiningTable_1, PepperShaker
  PepperShaker is in/on DiningTable_1
  Plate_0 is inside agent hand
  Apple, Microwave, Faucet are in/on CounterTop_0
  CounterTop_0, DishSponge are in/on Sink_Basin"""  
  ...
354: 2023/04/29 17:43:21 - 17:43:21: """Goal: Place(Sink_Basin)
  Visual observation: Drawer_0, Cabinet_0, Cabinet_1, Cabinet_2, Cabinet_3, Cabinet_4, CounterTop_0, Sink, Drawer_1, Drawer_2, Plate_0 [dirty], Apple, Sink_Basin, Microwave [toggled], DishSponge, Faucet, agent hand, DiningTable_1, PepperShaker
  PepperShaker is in/on DiningTable_1
  Plate_0 is inside agent hand
  Apple, Microwave, Faucet are in/on CounterTop_0
  CounterTop_0, DishSponge are in/on Sink_Basin"""  
  ...
355: 2023/04/29 17:43:22 - 17:43:23: """Goal: ToggleOn(Faucet)
  Visual observation: Drawer_0, Cabinet_0, Cabinet_1, Cabinet_2, Cabinet_3, Cabinet_4, CounterTop_0, Sink, Drawer_1, Drawer_2, Plate_0 [dirty], Apple, Sink_Basin, Microwave [toggled], DishSponge, Faucet, DiningTable_1, PepperShaker
  Apple, Microwave, Faucet are in/on CounterTop_0
  CounterTop_0, Plate_0, DishSponge are in/on Sink_Basin
  PepperShaker is in/on DiningTable_1
  Speech:
  2023-04-29 17:43:22.244717: There is a knife also there and the plate needs cleaning"""  
  ...
356: 2023/04/29 17:43:26 - 17:43:26: """Goal: ToggleOff(Faucet)
  Visual observation: Drawer_0, Cabinet_0, Cabinet_1, Cabinet_2, Cabinet_3, Cabinet_4, CounterTop_0, Sink, Drawer_1, Drawer_2, Plate_0, Apple, Sink_Basin, Microwave [toggled], DishSponge, Faucet, DiningTable_1, PepperShaker
  Apple, Microwave, Faucet are in/on CounterTop_0
  CounterTop_0, Plate_0, DishSponge are in/on Sink_Basin
  PepperShaker is in/on DiningTable_1"""  
  ...
357: 2023/04/29 17:43:27 - 17:43:27: """Goal: Pickup(Plate_0)
  Visual observation: Drawer_0, Cabinet_0, Cabinet_1, Cabinet_2, Cabinet_3, Cabinet_4, CounterTop_0, Sink, Drawer_1, Drawer_2, Plate_0, Apple, Sink_Basin, Microwave [toggled], DishSponge, Faucet, DiningTable_1, PepperShaker
  Apple, Microwave, Faucet are in/on CounterTop_0
  CounterTop_0, Plate_0, DishSponge are in/on Sink_Basin
  PepperShaker is in/on DiningTable_1"""  
  ...
358: 2023/04/29 17:43:28 - 17:43:34: """Goal: Place(DiningTable_1)
  Visual observation: Bowl_1 [filled], Plate_0, Bread_0, Knife_0, PepperShaker, SoapBottle, agent hand, DiningTable_1
  Plate_0 is inside agent hand
  SoapBottle, Bread_0, Knife_0, Bowl_1, PepperShaker are in/on DiningTable_1"""  
  ...
...
368: 2023/04/29 18:10:12 - 18:10:22: """Goal: Place(CounterTop_2)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Drawer_1, Drawer_2, Cabinet_0, Cabinet_1, Window, Sink, Drawer_6, Drawer_8, CounterTop_2, Bottle_0 [filled], Toaster [toggled], Tomato_0, CoffeeMachine [toggled], Sink_Basin, Faucet [toggled], agent hand
  Tomato_0, DishSponge_1, WineBottle_2, Bottle_0, Spoon_1, Lettuce_1 are in/on Sink_Basin
  Bowl_1 is inside agent hand
  CoffeeMachine, DishSponge_2, Toaster are in/on CounterTop_2
  Speech:
  2023-04-29 18:10:14.856709: you can use any container and fill it with water
  2023-04-29 18:10:22.212764: then just pour it on the plant please"""  
  ...
369: 2023/04/29 18:10:24 - 18:10:31: """Goal: ToggleOff(Faucet)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, CoffeeMachine [toggled], Sink_Basin, Faucet [toggled]
  Bowl_1, CoffeeMachine, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
370: 2023/04/29 18:10:34 - 18:10:34: """Goal: Pickup(Lettuce_1)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, CoffeeMachine [toggled], Sink_Basin, Faucet
  Bowl_1, CoffeeMachine, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
371: 2023/04/29 18:10:39 - 18:10:39: """Goal: Place(CounterTop_2)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, CoffeeMachine [toggled], Sink_Basin, Faucet, agent hand
  WineBottle_2, DishSponge_1, Bottle_0, Spoon_1 are in/on Sink_Basin
  Bowl_1, CoffeeMachine, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2
  Lettuce_1 is inside agent hand"""  
  ...
372: 2023/04/29 18:10:41 - 18:10:41: """Goal: Pickup(CreditCard_0)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Spoon_1, Tomato_0, CreditCard_0, WineBottle_2, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
373: 2023/04/29 18:10:44 - 18:10:44: """Goal: Place(CounterTop_2)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet, agent hand
  Spoon_1, Tomato_0, WineBottle_2, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2
  CreditCard_0 is inside agent hand"""  
  ...
374: 2023/04/29 18:10:47 - 18:10:47: """Goal: Pickup(Tomato_0)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Spoon_1, Tomato_0, WineBottle_2, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
375: 2023/04/29 18:10:50 - 18:10:50: """Goal: Place(CounterTop_2)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet, agent hand
  Spoon_1, WineBottle_2, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2
  Tomato_0 is inside agent hand"""  
  ...
376: 2023/04/29 18:10:52 - 18:10:52: """Goal: Pickup(Bottle_0)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Spoon_1, WineBottle_2, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, Tomato_0, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
377: 2023/04/29 18:10:57 - 18:10:57: """Goal: Place(Sink_Basin)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet, agent hand
  Spoon_1, WineBottle_2, DishSponge_1 are in/on Sink_Basin
  Bowl_1, Tomato_0, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2
  Bottle_0 is inside agent hand"""  
  ...
378: 2023/04/29 18:11:01 - 18:11:01: """Goal: ToggleOn(Faucet)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Spoon_1, WineBottle_2, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, Tomato_0, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
379: 2023/04/29 18:11:04 - 18:11:04: """Goal: ToggleOff(Faucet)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Spoon_1, WineBottle_2, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, Tomato_0, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
380: 2023/04/29 18:11:08 - 18:11:08: """Goal: Pickup(WineBottle_2)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Spoon_1, WineBottle_2, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, Tomato_0, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
381: 2023/04/29 18:11:10 - 18:11:10: """Goal: Place(CounterTop_2)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet, agent hand
  Spoon_1, DishSponge_1, Bottle_0 are in/on Sink_Basin
  Bowl_1, Tomato_0, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2
  WineBottle_2 is inside agent hand"""  
  ...
382: 2023/04/29 18:11:13 - 18:11:13: """Goal: Pickup(DishSponge_1)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Spoon_1, DishSponge_1, Bottle_0 are in/on Sink_Basin
  WineBottle_2, Bowl_1, Tomato_0, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
383: 2023/04/29 18:11:15 - 18:11:15: """Goal: Place(CounterTop_2)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet, agent hand
  DishSponge_1 is inside agent hand
  Spoon_1, Bottle_0 are in/on Sink_Basin
  WineBottle_2, Bowl_1, Tomato_0, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
384: 2023/04/29 18:11:18 - 18:11:18: """Goal: Pickup(Spoon_1)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Spoon_1, Bottle_0 are in/on Sink_Basin
  WineBottle_2, Bowl_1, Tomato_0, DishSponge_1, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
385: 2023/04/29 18:11:21 - 18:11:21: """Goal: Place(CounterTop_2)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet, agent hand
  WineBottle_2, Bowl_1, Tomato_0, DishSponge_1, CreditCard_0, Lettuce_1, Pan, Egg_1, DishSponge_2 are in/on CounterTop_2
  Spoon_1 is inside agent hand
  Bottle_0 is in/on Sink_Basin"""  
  ...
386: 2023/04/29 18:11:28 - 18:11:28: """Goal: Pickup(Bowl_1)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  WineBottle_2, Bowl_1, Tomato_0, DishSponge_1, CreditCard_0, Lettuce_1, Pan, Egg_1, Spoon_1, DishSponge_2 are in/on CounterTop_2
  Bottle_0 is in/on Sink_Basin"""  
  ...
387: 2023/04/29 18:11:30 - 18:11:30: """Goal: Place(Sink_Basin)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet, agent hand
  WineBottle_2, Tomato_0, DishSponge_1, CreditCard_0, Lettuce_1, Pan, Egg_1, Spoon_1, DishSponge_2 are in/on CounterTop_2
  Bowl_1 is inside agent hand
  Bottle_0 is in/on Sink_Basin"""  
  ...
388: 2023/04/29 18:11:42 - 18:11:42: """Goal: ToggleOn(Faucet)
  Visual observation: Bowl_1 [dirty], WineBottle_2 [filled], Egg_1, DishSponge_2, Lettuce_1, DishSponge_1, Spoon_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, Tomato_0, CreditCard_0, Sink_Basin, Faucet
  Bowl_1, Bottle_0 are in/on Sink_Basin
  WineBottle_2, Tomato_0, DishSponge_1, CreditCard_0, Lettuce_1, Pan, Egg_1, Spoon_1, DishSponge_2 are in/on CounterTop_2"""  
  ...
389: 2023/04/29 18:11:43 - 18:11:45: """Goal: ToggleOff(Faucet)
  Visual observation: Bowl_1 [filled], Lettuce_1, DishSponge_1, Spoon_1, Tomato_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, CreditCard_0, PaperTowelRoll_0, Sink_Basin, Faucet, WineBottle_2 [filled], Tomato_0
  PaperTowelRoll_0, Pan, Tomato_1, Lettuce_1, Tomato_0, WineBottle_2, DishSponge_1, CreditCard_0, Spoon_1 are in/on CounterTop_2
  Bottle_0, Bowl_1 are in/on Sink_Basin"""  
  ...
390: 2023/04/29 18:11:48 - 18:11:48: """Goal: Pickup(Bowl_1)
  Visual observation: Bowl_1 [filled], Lettuce_1, DishSponge_1, Spoon_1, Tomato_1, Cabinet_0, Window, Sink, CounterTop_2, Bottle_0 [filled], Pan, CreditCard_0, PaperTowelRoll_0, Sink_Basin, Faucet, WineBottle_2 [filled], Tomato_0
  PaperTowelRoll_0, Pan, Tomato_1, Lettuce_1, Tomato_0, WineBottle_2, DishSponge_1, CreditCard_0, Spoon_1 are in/on CounterTop_2
  Bottle_0, Bowl_1 are in/on Sink_Basin"""  
  ...
391: 2023/04/29 18:11:49 - 18:11:53: """Goal: Pour(HousePlant)
  Visual observation: Mug_2 [filled], PepperShaker_2, Bowl_1 [filled], Kettle_2, Bread_3, Tomato_1, StoveBurner_1, Cabinet_0, StoveBurner_3, Cabinet_2, Cabinet_3, Cabinet_5, CounterTop_2, Bread_0, HousePlant, Pan, Pot_0 [dirty, filled], PaperTowelRoll_0, agent hand, WineBottle_2 [filled], Lettuce_1, DishSponge_1, Spoon_1, Sink_Basin, Bottle_0 [filled], Tomato_0, CreditCard_0
  CreditCard_0, PaperTowelRoll_0, Pot_0, Lettuce_1, PepperShaker_2, Bread_3, Tomato_1, DishSponge_1, HousePlant, Pan, Tomato_0, Spoon_1, WineBottle_2, Mug_2, Bread_0 are in/on CounterTop_2
  Bowl_1 is inside agent hand
  Bottle_0 is in/on Sink_Basin"""  
  ...
...
393: 2023/04/30 15:48:29 - 15:48:50: """Goal: Pickup(Plate_0)
  Visual observation: Plate_1, Spatula_1, DiningTable, CoffeeMachine [toggled], Plate_0 [dirty], Bread_0, Toaster, Pan [dirty], SaltShaker_0, Tomato, Mug [dirty, filled]
  Mug is in/on CoffeeMachine
  Plate_0, SaltShaker_0, Bread_0, Tomato, Toaster, CoffeeMachine, Pan, Spatula_1, Plate_1, Mug are in/on DiningTable
  Speech:
  2023-04-30 15:48:33.182590: Hello
  2023-04-30 15:48:42.494592: clean the cookware
  2023-04-30 15:48:45.924369: 4 of them"""  
  ...
...
395: 2023/04/30 15:49:15 - 15:49:22: """Goal: Pickup(SoapBottle_0)
  Visual observation: Spoon_1, PepperShaker_1, Fork_2, Fork_1, Sink, CounterTop_2, SoapBottle_0, Lettuce_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet, CounterTop_1, DiningTable, Plate_0 [dirty]
  Plate_0 is in/on DiningTable
  HousePlant is in/on CounterTop_1"""  
  ...
396: 2023/04/30 15:49:25 - 15:49:25: """Goal: Place(CounterTop_1)
  Visual observation: Spoon_1, Fork_2, Fork_1, Sink, CounterTop_2, SoapBottle_0, Lettuce_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet, agent hand, DiningTable, Plate_0 [dirty]
  Spoon_1, Knife, Fork_2 are in/on Sink_Basin
  SoapBottle_0 is inside agent hand
  Plate_0 is in/on DiningTable"""  
  ...
397: 2023/04/30 15:49:27 - 15:49:27: """Goal: Pickup(Knife)
  Visual observation: Spoon_1, PepperShaker_1, Fork_2, Fork_1, Sink, CounterTop_2, SoapBottle_0, Lettuce_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet, CounterTop_1, DiningTable, Plate_0 [dirty]
  Fork_2, Spoon_1, Knife are in/on Sink_Basin
  Plate_0 is in/on DiningTable
  SoapBottle_0, HousePlant are in/on CounterTop_1"""  
  ...
398: 2023/04/30 15:49:30 - 15:49:45: """Goal: Place(CounterTop_2)
  Visual observation: Spoon_1, PepperShaker_1, Fork_2, Fork_1, Sink, CounterTop_2, SoapBottle_0, Lettuce_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet, CounterTop_1, DiningTable, Plate_0 [dirty], agent hand
  Fork_2, Spoon_1 are in/on Sink_Basin
  Plate_0 is in/on DiningTable
  SoapBottle_0, HousePlant are in/on CounterTop_1
  Knife is inside agent hand"""  
  ...
399: 2023/04/30 15:49:47 - 15:49:51: """Goal: Pickup(Spoon_1)
  Visual observation: Spoon_1, PepperShaker_1, Fork_1, Sink, Drawer_0, Drawer_3, CounterTop_2, SoapBottle_0, Lettuce_0, Window_0, Sink_Basin, Microwave [toggled], HousePlant, Faucet, CounterTop_1, DiningTable, Plate_0 [dirty], Knife
  Plate_0 is in/on DiningTable
  Spoon_1 is in/on Sink_Basin
  Microwave, Knife, Lettuce_0 are in/on CounterTop_2
  HousePlant, SoapBottle_0 are in/on CounterTop_1"""  
  ...
400: 2023/04/30 15:49:54 - 15:50:00: """Goal: Place(CounterTop_2)
  Visual observation: Spoon_1, PepperShaker_1, Fork_1, Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet, agent hand, CounterTop_1, SoapBottle_0, DiningTable, Plate_0 [dirty]
  Lettuce_0, Knife are in/on CounterTop_2
  Plate_0 is in/on DiningTable
  Spoon_1 is inside agent hand
  HousePlant, SoapBottle_0 are in/on CounterTop_1"""  
  ...
401: 2023/04/30 15:50:02 - 15:50:05: """Goal: Pickup(Fork_2)
  Visual observation: Spoon_1, PepperShaker_1, Fork_2, Fork_1, Sink, CounterTop_2, SoapBottle_0, Lettuce_0, Window_0, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet, CounterTop_1, DiningTable, Plate_0 [dirty]
  Knife, Lettuce_0, Microwave, Spoon_1 are in/on CounterTop_2
  Plate_0 is in/on DiningTable
  Fork_2 is in/on Sink_Basin
  HousePlant, SoapBottle_0 are in/on CounterTop_1"""  
  ...
402: 2023/04/30 15:50:08 - 15:50:12: """Goal: Place(CounterTop_1)
  Visual observation: SaltShaker_1, Pot_2 [dirty], Fork_2, Pot_1 [dirty, filled], StoveBurner_0, StoveBurner_1, StoveKnob_2, CounterTop_0, SoapBottle_0, Window_1, HousePlant, CounterTop_2, Spoon_1, agent hand, CounterTop_1, DiningTable, Plate_0 [dirty], Knife
  Knife, Spoon_1 are in/on CounterTop_2
  Plate_0 is in/on DiningTable
  Fork_2 is inside agent hand
  SoapBottle_0, HousePlant are in/on CounterTop_1"""  
  ...
...
404: 2023/04/30 15:50:16 - 15:50:21: """Goal: Place(Sink_Basin)
  Visual observation: PepperShaker_1, Pot_2 [dirty], Fork_1, Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Microwave [toggled], HousePlant, Faucet, Spoon_1, agent hand, CounterTop_1, Fork_2, SoapBottle_0, DiningTable, Plate_0 [dirty], Knife
  Plate_0 is in/on DiningTable
  HousePlant, SoapBottle_0, Fork_2 are in/on CounterTop_1
  Lettuce_0, Spoon_1, Microwave, Knife are in/on CounterTop_2
  Pot_2 is inside agent hand"""  
  ...
405: 2023/04/30 15:50:23 - 15:50:23: """Goal: ToggleOn(Faucet)
  Visual observation: Spoon_1, PepperShaker_1, Pot_2 [dirty], Fork_1, Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet, CounterTop_1, Fork_2, SoapBottle_0, DiningTable, Plate_0 [dirty]
  Microwave, Spoon_1, Knife, Lettuce_0 are in/on CounterTop_2
  Plate_0 is in/on DiningTable
  SoapBottle_0, Fork_2, HousePlant are in/on CounterTop_1
  Pot_2 is in/on Sink_Basin"""  
  ...
406: 2023/04/30 15:50:26 - 15:50:26: """Goal: ToggleOff(Faucet)
  Visual observation: Spoon_1, PepperShaker_1, Pot_2 [filled], Fork_1, Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], CounterTop_1, Fork_2, SoapBottle_0, DiningTable, Plate_0 [dirty]
  Microwave, Spoon_1, Knife, Lettuce_0 are in/on CounterTop_2
  Plate_0 is in/on DiningTable
  SoapBottle_0, Fork_2, HousePlant are in/on CounterTop_1
  Pot_2 is in/on Sink_Basin"""  
  ...
407: 2023/04/30 15:50:29 - 15:50:29: """Goal: Pickup(Pot_2)
  Visual observation: Spoon_1, PepperShaker_1, Pot_2 [filled], Fork_1, Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], CounterTop_1, Fork_2, SoapBottle_0, DiningTable, Plate_0 [dirty]
  Microwave, Spoon_1, Knife, Lettuce_0 are in/on CounterTop_2
  Plate_0 is in/on DiningTable
  SoapBottle_0, Fork_2, HousePlant are in/on CounterTop_1
  Pot_2 is in/on Sink_Basin"""  
  ...
408: 2023/04/30 15:50:30 - 15:50:35: """Goal: Place(StoveBurner_1)
  Visual observation: Pot_2 [filled], Pot_1 [dirty, filled], StoveBurner_0, StoveBurner_1, StoveKnob_2, CounterTop_0, Window_1, CounterTop_2, Spoon_1, agent hand, CounterTop_1, Fork_2, SoapBottle_0, DiningTable, Plate_0 [dirty], Knife
  Pot_2 is inside agent hand
  Spoon_1, Knife are in/on CounterTop_2
  Fork_2, SoapBottle_0 are in/on CounterTop_1
  Plate_0 is in/on DiningTable"""  
  ...
...
410: 2023/04/30 15:50:40 - 15:50:44: """Goal: Place(Sink_Basin)
  Visual observation: Spoon_1, PepperShaker_1, Pot_1 [dirty, filled], Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Knife, Microwave [toggled], HousePlant, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, agent hand, SoapBottle_0, DiningTable, Plate_0 [dirty]
  Spoon_1, Microwave, Lettuce_0, Knife are in/on CounterTop_2
  Pot_1 is inside agent hand
  Pot_2 is in/on StoveBurner_1
  SoapBottle_0, Fork_2, HousePlant are in/on CounterTop_1
  Plate_0 is in/on DiningTable"""  
  ...
411: 2023/04/30 15:50:47 - 15:50:47: """Goal: ToggleOn(Faucet)
  Visual observation: Spoon_1, PepperShaker_1, Fork_1, Pot_1 [dirty, filled], Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, SoapBottle_0, DiningTable, Plate_0 [dirty]
  Microwave, Knife, Spoon_1, Lettuce_0 are in/on CounterTop_2
  Fork_2, SoapBottle_0, HousePlant are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Plate_0 is in/on DiningTable
  Pot_1 is in/on Sink_Basin"""  
  ...
412: 2023/04/30 15:50:50 - 15:50:50: """Goal: ToggleOff(Faucet)
  Visual observation: Spoon_1, PepperShaker_1, Fork_1, Pot_1 [filled], Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, SoapBottle_0, DiningTable, Plate_0 [dirty]
  Microwave, Knife, Spoon_1, Lettuce_0 are in/on CounterTop_2
  Fork_2, SoapBottle_0, HousePlant are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Plate_0 is in/on DiningTable
  Pot_1 is in/on Sink_Basin"""  
  ...
413: 2023/04/30 15:50:52 - 15:50:52: """Goal: Pickup(Pot_1)
  Visual observation: Spoon_1, PepperShaker_1, Fork_1, Pot_1 [filled], Sink, CounterTop_2, Lettuce_0, Window_0, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, SoapBottle_0, DiningTable, Plate_0 [dirty]
  Microwave, Knife, Spoon_1, Lettuce_0 are in/on CounterTop_2
  Fork_2, SoapBottle_0, HousePlant are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Plate_0 is in/on DiningTable
  Pot_1 is in/on Sink_Basin"""  
  ...
414: 2023/04/30 15:50:54 - 15:51:01: """Goal: Place(StoveBurner_3)
  Visual observation: Pot_2 [filled], Pot_1 [filled], StoveBurner_1, StoveKnob_2, CounterTop_0, Window_1, CounterTop_2, Spoon_1, CounterTop_1, Fork_2, agent hand, SoapBottle_0, DiningTable, Plate_0 [dirty], Knife
  Knife, Spoon_1 are in/on CounterTop_2
  Fork_2, SoapBottle_0 are in/on CounterTop_1
  Pot_1 is inside agent hand
  Pot_2 is in/on StoveBurner_1
  Plate_0 is in/on DiningTable"""  
  ...
...
416: 2023/04/30 15:51:38 - 15:51:43: """Goal: Place(Sink_Basin)
  Visual observation: Spoon_1, PepperShaker_1, Sink, CounterTop_2, Lettuce_0, Window_0, Pan [dirty], Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], SoapBottle_0, DiningTable, Plate_0 [dirty], agent hand
  Pot_1 is in/on StoveBurner_3
  Spoon_1, Microwave, Lettuce_0, Knife are in/on CounterTop_2
  Plate_0 is in/on DiningTable
  Pan is inside agent hand
  Fork_2, SoapBottle_0, HousePlant are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1"""  
  ...
417: 2023/04/30 15:51:47 - 15:51:47: """Goal: ToggleOn(Faucet)
  Visual observation: Spoon_1, PepperShaker_1, Fork_1, Sink, CounterTop_2, Lettuce_0, Window_0, Pan [dirty], Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], SoapBottle_0, DiningTable, Plate_0 [dirty]
  SoapBottle_0, Fork_2, HousePlant are in/on CounterTop_1
  Spoon_1, Knife, Lettuce_0, Microwave are in/on CounterTop_2
  Pan is in/on Sink_Basin
  Pot_2 is in/on StoveBurner_1
  Pot_1 is in/on StoveBurner_3
  Plate_0 is in/on DiningTable"""  
  ...
418: 2023/04/30 15:51:50 - 15:51:50: """Goal: ToggleOff(Faucet)
  Visual observation: Spoon_1, PepperShaker_1, Fork_1, Sink, CounterTop_2, Lettuce_0, Window_0, Pan, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], SoapBottle_0, DiningTable, Plate_0 [dirty]
  SoapBottle_0, Fork_2, HousePlant are in/on CounterTop_1
  Spoon_1, Knife, Lettuce_0, Microwave are in/on CounterTop_2
  Pan is in/on Sink_Basin
  Pot_2 is in/on StoveBurner_1
  Pot_1 is in/on StoveBurner_3
  Plate_0 is in/on DiningTable"""  
  ...
419: 2023/04/30 15:51:52 - 15:51:52: """Goal: Pickup(Pan)
  Visual observation: Spoon_1, PepperShaker_1, Fork_1, Sink, CounterTop_2, Lettuce_0, Window_0, Pan, Sink_Basin, Knife, Microwave [toggled], HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], SoapBottle_0, DiningTable, Plate_0 [dirty]
  SoapBottle_0, Fork_2, HousePlant are in/on CounterTop_1
  Spoon_1, Knife, Lettuce_0, Microwave are in/on CounterTop_2
  Pan is in/on Sink_Basin
  Pot_2 is in/on StoveBurner_1
  Pot_1 is in/on StoveBurner_3
  Plate_0 is in/on DiningTable"""  
  ...
420: 2023/04/30 15:51:54 - 15:52:06: """Goal: Place(DiningTable)
  Visual observation: Bowl_2 [filled], Plate_1, DiningTable, Bread_0, Pan, SaltShaker_0, ButterKnife_0, CounterTop_2, Spoon_1, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], SoapBottle_0, Plate_0 [dirty], agent hand, Knife
  Spoon_1, Knife are in/on CounterTop_2
  Fork_2, SoapBottle_0 are in/on CounterTop_1
  SaltShaker_0, ButterKnife_0, Bread_0, Plate_0, Plate_1, Bowl_2 are in/on DiningTable
  Pot_1 is in/on StoveBurner_3
  Pan is inside agent hand
  Pot_2 is in/on StoveBurner_1"""  
  ...
...
422: 2023/04/30 15:52:21 - 15:52:27: """Goal: Place(Sink_Basin)
  Visual observation: Fork_1, SoapBottle_0, Plate_0 [dirty], Window_0, Sink_Basin, Knife, HousePlant, Faucet [toggled], CounterTop_2, Spoon_1, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], agent hand, DiningTable, Pan
  Plate_0 is inside agent hand
  Spoon_1, Knife are in/on CounterTop_2
  SoapBottle_0, HousePlant, Fork_2 are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Pot_1 is in/on StoveBurner_3
  Pan is in/on DiningTable
  Speech:
  2023-04-30 15:52:21.248559: Searching for it"""  
  ...
423: 2023/04/30 15:52:30 - 15:52:30: """Goal: ToggleOn(Faucet)
  Visual observation: PepperShaker_1, Fork_1, SoapBottle_0, Plate_0 [dirty], Window_0, Sink_Basin, Knife, HousePlant, Faucet [toggled], CounterTop_2, Spoon_1, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], DiningTable, Pan
  Pot_1 is in/on StoveBurner_3
  HousePlant, SoapBottle_0, Fork_2 are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Pan is in/on DiningTable
  Knife, Spoon_1 are in/on CounterTop_2
  Plate_0 is in/on Sink_Basin"""  
  ...
424: 2023/04/30 15:52:33 - 15:52:33: """Goal: ToggleOff(Faucet)
  Visual observation: PepperShaker_1, Fork_1, SoapBottle_0, Plate_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet [toggled], CounterTop_2, Spoon_1, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], DiningTable, Pan
  Pot_1 is in/on StoveBurner_3
  HousePlant, SoapBottle_0, Fork_2 are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Pan is in/on DiningTable
  Knife, Spoon_1 are in/on CounterTop_2
  Plate_0 is in/on Sink_Basin"""  
  ...
425: 2023/04/30 15:52:36 - 15:52:36: """Goal: Pickup(Plate_0)
  Visual observation: PepperShaker_1, Fork_1, SoapBottle_0, Plate_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet [toggled], CounterTop_2, Spoon_1, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], Sink, DiningTable, Pan
  Pot_1 is in/on StoveBurner_3
  Fork_1, Faucet, PepperShaker_1 are in/on Sink
  HousePlant, Fork_2, SoapBottle_0 are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Knife, Spoon_1 are in/on CounterTop_2
  Pan is in/on DiningTable
  Plate_0 is in/on Sink_Basin"""  
  ...
426: 2023/04/30 15:52:40 - 15:52:40: """Goal: Place(CounterTop_1)
  Visual observation: Fork_1, SoapBottle_0, Plate_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet [toggled], CounterTop_2, Spoon_1, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], Sink, agent hand, DiningTable, Pan
  Spoon_1, Knife are in/on CounterTop_2
  Faucet, Fork_1 are in/on Sink
  Plate_0 is inside agent hand
  SoapBottle_0, HousePlant, Fork_2 are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Pot_1 is in/on StoveBurner_3
  Pan is in/on DiningTable"""  
  ...
427: 2023/04/30 15:52:44 - 15:52:59: """Goal: Open(Fridge)
  Visual observation: GarbageCan, CounterTop_2, Spoon_1, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], SoapBottle_0, Plate_0, DiningTable, Pan, Knife
  Plate_0, SoapBottle_0, Fork_2 are in/on CounterTop_1
  Pot_1 is in/on StoveBurner_3
  Pan is in/on DiningTable
  Pot_2 is in/on StoveBurner_1
  Knife, Spoon_1 are in/on CounterTop_2
  Speech:
  2023-04-30 15:52:52.867414: check the fridge"""  
  ...
...
429: 2023/04/30 15:53:09 - 15:53:16: """Goal: Place(Sink_Basin)
  Visual observation: Spoon_1, Fork_2, Fork_1, Sink, CounterTop_2, SoapBottle_0, Pot_0 [dirty, filled], Plate_0, Lettuce_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, StoveBurner_3, Pot_1 [filled], agent hand, DiningTable, Pan
  Plate_0, Fork_2, SoapBottle_0, HousePlant are in/on CounterTop_1
  Pot_0 is inside agent hand
  Spoon_1, Knife, Lettuce_0 are in/on CounterTop_2
  Pot_2 is in/on StoveBurner_1
  Pot_1 is in/on StoveBurner_3
  Pan is in/on DiningTable"""  
  ...
430: 2023/04/30 15:53:18 - 15:53:23: """Goal: ToggleOn(Faucet)
  Visual observation: Spoon_1, PepperShaker_1, Fork_2, Fork_1, Sink, CounterTop_2, SoapBottle_0, Pot_0 [dirty, filled], Plate_0, Lettuce_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, StoveBurner_3, Pot_1 [filled], DiningTable, Pan
  Pot_2 is in/on StoveBurner_1
  PepperShaker_1, Faucet, Fork_1 are in/on Sink
  Knife, Lettuce_0, Spoon_1 are in/on CounterTop_2
  Pot_0 is in/on Sink_Basin
  SoapBottle_0, Fork_2, Plate_0, HousePlant are in/on CounterTop_1
  Pan is in/on DiningTable
  Pot_1 is in/on StoveBurner_3
  Speech:
  2023-04-30 15:53:18.327117: Good"""  
  ...
431: 2023/04/30 15:53:24 - 15:53:29: """Goal: ToggleOff(Faucet)
  Visual observation: Spoon_1, PepperShaker_1, Fork_2, Fork_1, Sink, CounterTop_2, SoapBottle_0, Pot_0 [filled], Plate_0, Lettuce_0, Window_0, Sink_Basin, Knife, HousePlant, Faucet [toggled], StoveBurner_1, Pot_2 [filled], CounterTop_1, StoveBurner_3, Pot_1 [filled], DiningTable, Pan
  Pot_2 is in/on StoveBurner_1
  PepperShaker_1, Faucet, Fork_1 are in/on Sink
  Knife, Lettuce_0, Spoon_1 are in/on CounterTop_2
  Pot_0 is in/on Sink_Basin
  SoapBottle_0, Fork_2, Plate_0, HousePlant are in/on CounterTop_1
  Pan is in/on DiningTable
  Pot_1 is in/on StoveBurner_3"""  
  ...
432: 2023/04/30 15:53:49 - 15:54:09: """Goal: LookDown()
  Visual observation: CounterTop_2, Spoon_1, StoveBurner_1, Pot_2 [filled], CounterTop_1, Fork_2, StoveBurner_3, Pot_1 [filled], SoapBottle_0, Sink_Basin, Pot_0 [filled], Plate_0, DiningTable, Pan, Knife
  Pot_1 is in/on StoveBurner_3
  Spoon_1, Knife are in/on CounterTop_2
  Fork_2, Plate_0, SoapBottle_0 are in/on CounterTop_1
  Pot_2 is in/on StoveBurner_1
  Pot_0 is in/on Sink_Basin
  Pan is in/on DiningTable
  Speech:
  2023-04-30 15:54:08.155385: Completed"""  
  ...
433: 2023/05/01 10:32:32 - 10:34:33: """Goal: Open(Microwave)
  Visual observation: PepperShaker_1, Knife_3, Bread_2, Fork_1, Bread_1, Cup_1 [dirty, filled], DishSponge_1, Drawer_0, Cabinet_0, Cabinet_1, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Cabinet_9, CounterTop_0, Sink, Drawer_1, Floor, Spatula, Sink_Basin, Microwave, Faucet, Bowl_0 [dirty, filled]
  Fork_1, PepperShaker_1, CounterTop_0, DishSponge_1, Spatula are in/on Sink_Basin
  Bread_1, Knife_3, Microwave, Faucet are in/on CounterTop_0
  Speech:
  2023-05-01 10:32:33.604331: hello!
  2023-05-01 10:32:57.765313: The task is to boil the potato by cooking it in water.
  2023-05-01 10:33:35.642745: The potato is in what looks like a pan on the same table as the toaster
  2023-05-01 10:33:41.261753: right next to where you started
  2023-05-01 10:33:58.743685: it's a white table
  2023-05-01 10:34:33.132038: with a toaster"""  
  ...
434: 2023/05/01 10:34:49 - 10:34:49: """Goal: Pickup(Apple_2)
  Visual observation: PepperShaker_1, Knife_3, Apple_2, Bread_2, Fork_1, Bread_1, Knife_1, Cup_1 [dirty, filled], DishSponge_1, Drawer_0, Cabinet_0, Cabinet_1, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Cabinet_9, CounterTop_0, Sink, Drawer_1, Floor, Spatula, Sink_Basin, ButterKnife_0, Microwave [open], Faucet, Bowl_0 [dirty, filled]
  Faucet, Knife_3, ButterKnife_0, Bread_1, Microwave, Apple_2, Knife_1 are in/on CounterTop_0
  Fork_1, CounterTop_0, DishSponge_1, PepperShaker_1, Spatula are in/on Sink_Basin
  ButterKnife_0, Apple_2, Knife_1 are in/on Microwave"""  
  ...
435: 2023/05/01 10:34:53 - 10:35:19: """Goal: Place(CounterTop_0)
  Visual observation: Apple_2, Egg_1, Bowl_2 [dirty, filled], Bread_1, ButterKnife_1, Plate_1, Cabinet_2, Cabinet_3, Cabinet_4, Cabinet_5, Cabinet_6, CounterTop_0, Sink, Drawer_1, Drawer_2, Floor, Plate_0 [dirty], GarbageCan, agent hand, Sink_Basin
  Plate_0 is in/on Cabinet_6
  Egg_1, Bowl_2, Bread_1 are in/on CounterTop_0
  GarbageCan is in/on Floor
  Apple_2 is inside agent hand
  CounterTop_0 is in/on Sink_Basin"""  
  ...
436: 2023/05/01 10:35:22 - 10:35:47: """Goal: Pickup(Potato_2)
  Visual observation: Pan_1 [dirty], Bowl_3 [dirty], Potato_2, CounterTop_1, Floor, Fork_0, Lettuce_0, PepperShaker_0, Mug_0 [dirty], DiningTable_0, CounterTop_0, Apple_2, Sink_Basin, DiningTable_1
  Fork_0, PepperShaker_0, Potato_2, Lettuce_0, Mug_0, Pan_1 are in/on DiningTable_1
  PepperShaker_0, Potato_2 are in/on Pan_1
  CounterTop_0 is in/on Sink_Basin
  DiningTable_0 is in/on Floor
  Apple_2 is in/on CounterTop_0
  Bowl_3 is in/on CounterTop_1"""  
  ...
...
445: 2023/05/01 17:33:32 - 17:35:07: """Goal: Place(CounterTop_0)
  Visual observation: Book_1, Plate, PaperTowelRoll_0, PepperShaker, Lettuce_0, ButterKnife, CounterTop_0, agent hand
  PepperShaker, Book_1, ButterKnife, Plate, PaperTowelRoll_0 are in/on CounterTop_0
  Lettuce_0 is inside agent hand"""  
  ...
...
449: 2023/05/01 17:37:10 - 17:37:25: """Goal: ToggleOff(Faucet)
  Visual observation: Lettuce_1, Spatula_2, Spatula_1, Apple_1, Cabinet_0, Window, Sink, Cabinet_5, CounterTop_2, Knife, Bread, HousePlant, Vase_1, CoffeeMachine [toggled], Sink_Basin, Faucet [toggled], CounterTop_0, Lettuce_0_Sliced_7, Lettuce_0_Sliced_6, Lettuce_0_Sliced_5, Lettuce_0_Sliced_4, Lettuce_0_Sliced_3, Lettuce_0_Sliced_2, Lettuce_0_Sliced_1, Lettuce_0_Sliced_0, ButterKnife
  Lettuce_0_Sliced_7, Lettuce_0_Sliced_1, Lettuce_0_Sliced_4, Lettuce_0_Sliced_0, Lettuce_0_Sliced_3, Lettuce_0_Sliced_6, Lettuce_0_Sliced_2, Lettuce_0_Sliced_5, ButterKnife are in/on CounterTop_0
  Spatula_2, Vase_1, Spatula_1, Knife, Apple_1, Lettuce_1 are in/on Sink_Basin"""  
  ...
450: 2023/05/01 17:37:39 - 17:37:39: """Goal: Pickup(Apple_1)
  Visual observation: Lettuce_1, Spatula_2, Spatula_1, Apple_1, Cabinet_0, Window, Sink, Cabinet_5, CounterTop_2, Knife, Bread, HousePlant, Vase_1, CoffeeMachine [toggled], Sink_Basin, Faucet, CounterTop_0, Lettuce_0_Sliced_7, Lettuce_0_Sliced_6, Lettuce_0_Sliced_5, Lettuce_0_Sliced_4, Lettuce_0_Sliced_3, Lettuce_0_Sliced_2, Lettuce_0_Sliced_1, Lettuce_0_Sliced_0, ButterKnife
  Lettuce_0_Sliced_7, Lettuce_0_Sliced_1, Lettuce_0_Sliced_4, Lettuce_0_Sliced_0, Lettuce_0_Sliced_3, Lettuce_0_Sliced_6, Lettuce_0_Sliced_2, Lettuce_0_Sliced_5, ButterKnife are in/on CounterTop_0
  Spatula_2, Vase_1, Spatula_1, Knife, Apple_1, Lettuce_1 are in/on Sink_Basin"""  
  ...
451: 2023/05/01 17:37:52 - 17:37:52: """Goal: Place(CounterTop_2)
  Visual observation: Lettuce_1, Spatula_2, Spatula_1, Apple_1, Cabinet_0, Window, Sink, Cabinet_5, CounterTop_2, Knife, Bread, HousePlant, Vase_1, CoffeeMachine [toggled], Sink_Basin, Faucet, CounterTop_0, Lettuce_0_Sliced_7, Lettuce_0_Sliced_6, Lettuce_0_Sliced_5, Lettuce_0_Sliced_4, Lettuce_0_Sliced_3, Lettuce_0_Sliced_2, Lettuce_0_Sliced_1, Lettuce_0_Sliced_0, agent hand, ButterKnife
  Lettuce_0_Sliced_7, Lettuce_0_Sliced_1, Lettuce_0_Sliced_4, Lettuce_0_Sliced_0, Lettuce_0_Sliced_3, Lettuce_0_Sliced_6, Lettuce_0_Sliced_2, Lettuce_0_Sliced_5, ButterKnife are in/on CounterTop_0
  Spatula_2, Vase_1, Spatula_1, Knife, Lettuce_1 are in/on Sink_Basin
  Apple_1 is inside agent hand"""  
  ...
452: 2023/05/01 17:37:55 - 17:38:28: """Goal: Pickup(Tomato_0)
  Visual observation: SoapBottle_2, Drawer_0, CounterTop_1, Drawer_3, Drawer_4, Drawer_5, Cabinet_4, Drawer_7, Cabinet_7, Bottle [filled], Shelf_0, SoapBottle_0, Shelf_1, Pan, Tomato_0, Spatula_0, Shelf_2, SaltShaker, DishSponge, ShelvingUnit, CounterTop_0, Lettuce_0_Sliced_7, Lettuce_0_Sliced_6, Lettuce_0_Sliced_5, Lettuce_0_Sliced_4, Lettuce_0_Sliced_3, Lettuce_0_Sliced_2, Lettuce_0_Sliced_1, Lettuce_0_Sliced_0, CounterTop_2, Apple_1, Floor, ButterKnife
  Lettuce_0_Sliced_0, Lettuce_0_Sliced_1, Lettuce_0_Sliced_5, Lettuce_0_Sliced_6, ButterKnife, Lettuce_0_Sliced_4, Lettuce_0_Sliced_7, Lettuce_0_Sliced_2, Lettuce_0_Sliced_3 are in/on CounterTop_0
  Pan, SaltShaker, SoapBottle_0, Spatula_0 are in/on CounterTop_1
  SoapBottle_2, Tomato_0, Bottle are in/on Shelf_0
  Apple_1 is in/on CounterTop_2
  ShelvingUnit is in/on Floor"""  
  ...
...
486: 2023/05/02 12:11:41 - 12:11:53: """Goal: Place(Sink)
  Visual observation: Bowl_1, Cabinet_0, Cabinet_1, Faucet, Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [dirty, filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, agent hand, Fork
  SoapBottle, Cup_0, ButterKnife_0, Egg_0, Faucet, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  Fork is inside agent hand"""  
  ...
487: 2023/05/02 12:11:58 - 12:11:58: """Goal: Pickup(ButterKnife_0)
  Visual observation: Bowl_1, Cabinet_0, Cabinet_1, Faucet, Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [dirty, filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  SoapBottle, Cup_0, ButterKnife_0, Egg_0, Faucet, Fork, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop"""  
  ...
488: 2023/05/02 12:12:00 - 12:12:00: """Goal: Place(Sink_Basin)
  Visual observation: Bowl_1, Cabinet_0, Cabinet_1, Faucet, Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [dirty, filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork, agent hand
  SoapBottle, Cup_0, Egg_0, Faucet, Fork, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  ButterKnife_0 is inside agent hand"""  
  ...
489: 2023/05/02 12:12:05 - 12:12:05: """Goal: ToggleOn(Faucet)
  Visual observation: Bowl_1, Cabinet_0, Cabinet_1, Faucet, Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [dirty, filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, Fork, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  Bowl_1, ButterKnife_0 are in/on Sink_Basin"""  
  ...
490: 2023/05/02 12:12:08 - 12:12:08: """Goal: ToggleOff(Faucet)
  Visual observation: Bowl_1 [filled], Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, Fork, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  Bowl_1, ButterKnife_0 are in/on Sink_Basin"""  
  ...
491: 2023/05/02 12:12:12 - 12:12:12: """Goal: Pickup(ButterKnife_0)
  Visual observation: Bowl_1 [filled], Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, Fork, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  Bowl_1, ButterKnife_0 are in/on Sink_Basin"""  
  ...
492: 2023/05/02 12:12:16 - 12:12:16: """Goal: Place(CounterTop)
  Visual observation: Bowl_1 [filled], Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork, agent hand
  SoapBottle, Cup_0, Egg_0, Faucet, Fork, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  ButterKnife_0 is inside agent hand"""  
  ...
493: 2023/05/02 12:12:19 - 12:12:19: """Goal: Pickup(Bowl_1)
  Visual observation: Bowl_1 [filled], Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, Fork, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop"""  
  ...
494: 2023/05/02 12:12:22 - 12:12:22: """Goal: Pour(Sink_Basin)
  Visual observation: Bowl_1 [filled], Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, agent hand, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Fork, Faucet, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Bowl_1 is inside agent hand"""  
  ...
495: 2023/05/02 12:12:25 - 12:12:25: """Goal: Place(CounterTop)
  Visual observation: Bowl_1 [filled], Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, agent hand, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Fork, Faucet, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Pot, DishSponge_0, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Bowl_1 is inside agent hand"""  
  ...
496: 2023/05/02 12:12:27 - 12:13:16: """Goal: Pickup(Bowl_0)
  Visual observation: PepperShaker_1, ButterKnife_2, Egg_2, Bowl_0 [dirty], Potato_0, Fridge, Pan_0, Drawer_2, Drawer_3, Drawer_4, SideTable, Drawer_5, Drawer_6, Drawer_7, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Floor, Knife, Sink, Fork, ButterKnife_0
  Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_5, Bowl_1, Knife, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bread_Sliced_6, Bread_Sliced_4, ButterKnife_0 are in/on CounterTop
  Egg_2, ButterKnife_2, Pan_0, Potato_0, Bowl_0, PepperShaker_1 are in/on SideTable
  Drawer_6, Fridge, Drawer_5, SideTable are in/on Floor
  Fork is in/on Sink"""  
  ...
497: 2023/05/02 12:13:17 - 12:13:29: """Goal: Place(Sink)
  Visual observation: Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [dirty], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, agent hand, Fork
  Bread_Sliced_3, Bread_Sliced_2, HousePlant, Bread_Sliced_1, Bread_Sliced_7, Bread_Sliced_5, ButterKnife_0, Bread_Sliced_8, Bread_Sliced_6, Bowl_1, Potato_1, Knife, DishSponge_0, Bread_Sliced_4 are in/on CounterTop
  Fork, Faucet, Cup_0, Egg_0, Spatula_0, SoapBottle are in/on Sink
  Bowl_0 is inside agent hand"""  
  ...
498: 2023/05/02 12:13:31 - 12:13:35: """Goal: Pickup(Cup_0)
  Visual observation: Cabinet_0, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [dirty], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, Fork
  Bread_Sliced_6, ButterKnife_0, DishSponge_0, Knife, Pot, Bread_Sliced_7, Bread_Sliced_1, Potato_1, Bowl_1, Bread_Sliced_5, HousePlant, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_8 are in/on CounterTop
  Spatula_0, Bowl_0, SoapBottle, Fork, Faucet, Egg_0, PepperShaker_0, Cup_0 are in/on Sink"""  
  ...
499: 2023/05/02 12:13:38 - 12:13:38: """Goal: Place(Sink)
  Visual observation: Cabinet_0, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [dirty], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, Fork, agent hand
  Bread_Sliced_6, ButterKnife_0, DishSponge_0, Knife, Pot, Bread_Sliced_7, Bread_Sliced_1, Potato_1, Bowl_1, Bread_Sliced_5, HousePlant, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_8 are in/on CounterTop
  Spatula_0, Bowl_0, SoapBottle, Fork, Faucet, Egg_0, PepperShaker_0 are in/on Sink
  Cup_0 is inside agent hand"""  
  ...
500: 2023/05/02 12:13:42 - 12:13:42: """Goal: Pickup(Bowl_0)
  Visual observation: Cabinet_0, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [dirty], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, Fork
  Bread_Sliced_6, ButterKnife_0, DishSponge_0, Knife, Pot, Bread_Sliced_7, Bread_Sliced_1, Potato_1, Bowl_1, Bread_Sliced_5, HousePlant, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_8 are in/on CounterTop
  Spatula_0, Bowl_0, SoapBottle, Fork, Faucet, Egg_0, PepperShaker_0, Cup_0 are in/on Sink"""  
  ...
501: 2023/05/02 12:13:43 - 12:13:46: """Goal: Place(Sink_Basin)
  Visual observation: Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [dirty], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, agent hand, Fork
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Pot, Bread_Sliced_7, DishSponge_0, Bowl_1, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  PepperShaker_0, Fork, Spatula_0, Faucet, SoapBottle, Cup_0, Egg_0 are in/on Sink
  Bowl_0 is inside agent hand"""  
  ...
502: 2023/05/02 12:13:48 - 12:13:50: """Goal: ToggleOn(Faucet)
  Visual observation: Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [dirty], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, Fork
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Pot, Bread_Sliced_7, DishSponge_0, Bowl_1, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  PepperShaker_0, Spatula_0, Faucet, SoapBottle, Cup_0, Egg_0, Fork are in/on Sink
  Bowl_0 is in/on Sink_Basin
  Speech:
  2023-05-02 12:13:48.917900: clean all of them. 4 in total"""  
  ...
503: 2023/05/02 12:13:55 - 12:13:55: """Goal: ToggleOff(Faucet)
  Visual observation: Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, Fork
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Pot, Bread_Sliced_7, DishSponge_0, Bowl_1, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  PepperShaker_0, Spatula_0, Faucet, SoapBottle, Cup_0, Egg_0, Fork are in/on Sink
  Bowl_0 is in/on Sink_Basin"""  
  ...
504: 2023/05/02 12:14:00 - 12:14:00: """Goal: Pickup(Bowl_0)
  Visual observation: Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, Fork
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Pot, Bread_Sliced_7, DishSponge_0, Bowl_1, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  PepperShaker_0, Spatula_0, Faucet, SoapBottle, Cup_0, Egg_0, Fork are in/on Sink
  Bowl_0 is in/on Sink_Basin"""  
  ...
505: 2023/05/02 12:14:02 - 12:14:03: """Goal: Pour(Sink_Basin)
  Visual observation: Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, agent hand, Fork
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Pot, Bread_Sliced_7, DishSponge_0, Bowl_1, Knife, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  PepperShaker_0, Fork, Spatula_0, Faucet, SoapBottle, Cup_0, Egg_0 are in/on Sink
  Bowl_0 is inside agent hand
  Speech:
  2023-05-02 12:14:02.810669: clean all of them. 4 in total"""  
  ...
506: 2023/05/02 12:14:06 - 12:14:09: """Goal: Place(CounterTop)
  Visual observation: Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, agent hand, Fork
  Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_5, Knife, Bowl_1, ButterKnife_0, Bread_Sliced_3, Bread_Sliced_2, HousePlant, Bread_Sliced_1, Potato_1, Bread_Sliced_6, Bread_Sliced_4, DishSponge_0 are in/on CounterTop
  Bowl_0 is inside agent hand
  Faucet, Fork, Cup_0, Spatula_0, SoapBottle are in/on Sink"""  
  ...
507: 2023/05/02 12:14:11 - 12:14:16: """Goal: Pickup(Fork)
  Visual observation: Cabinet_0, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Knife, Bowl_0 [filled], Fork
  Bread_Sliced_3, HousePlant, Bread_Sliced_2, Bread_Sliced_1, Bread_Sliced_7, Bread_Sliced_5, Bowl_0, Pot, Bread_Sliced_8, Bread_Sliced_6, Knife, Potato_1, ButterKnife_0, Bowl_1, DishSponge_0, Bread_Sliced_4 are in/on CounterTop
  Spatula_0, SoapBottle, Cup_0, PepperShaker_0, Fork, Faucet, Egg_0 are in/on Sink"""  
  ...
508: 2023/05/02 12:14:18 - 12:14:21: """Goal: Place(Sink_Basin)
  Visual observation: Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, agent hand, Fork
  Bread_Sliced_6, ButterKnife_0, DishSponge_0, Bread_Sliced_7, Bowl_1, Bread_Sliced_1, Potato_1, Knife, Bread_Sliced_5, HousePlant, Bread_Sliced_4, Bread_Sliced_3, Bowl_0, Bread_Sliced_2, Bread_Sliced_8 are in/on CounterTop
  PepperShaker_0, Faucet, Cup_0, Egg_0, Spatula_0, SoapBottle are in/on Sink
  Fork is inside agent hand"""  
  ...
509: 2023/05/02 12:14:24 - 12:14:24: """Goal: ToggleOn(Faucet)
  Visual observation: Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  Fork is in/on Sink_Basin
  Bread_Sliced_6, ButterKnife_0, DishSponge_0, Bread_Sliced_7, Bowl_1, Bread_Sliced_1, Potato_1, Knife, Bread_Sliced_5, HousePlant, Bread_Sliced_4, Bread_Sliced_3, Bowl_0, Bread_Sliced_2, Bread_Sliced_8 are in/on CounterTop
  PepperShaker_0, Faucet, Cup_0, Egg_0, Spatula_0, SoapBottle are in/on Sink"""  
  ...
510: 2023/05/02 12:14:27 - 12:14:27: """Goal: ToggleOff(Faucet)
  Visual observation: Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  Fork is in/on Sink_Basin
  Bread_Sliced_6, ButterKnife_0, DishSponge_0, Bread_Sliced_7, Bowl_1, Bread_Sliced_1, Potato_1, Knife, Bread_Sliced_5, HousePlant, Bread_Sliced_4, Bread_Sliced_3, Bowl_0, Bread_Sliced_2, Bread_Sliced_8 are in/on CounterTop
  PepperShaker_0, Faucet, Cup_0, Egg_0, Spatula_0, SoapBottle are in/on Sink"""  
  ...
511: 2023/05/02 12:14:30 - 12:14:30: """Goal: Pickup(Fork)
  Visual observation: Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  Fork is in/on Sink_Basin
  Bread_Sliced_6, ButterKnife_0, DishSponge_0, Bread_Sliced_7, Bowl_1, Bread_Sliced_1, Potato_1, Knife, Bread_Sliced_5, HousePlant, Bread_Sliced_4, Bread_Sliced_3, Bowl_0, Bread_Sliced_2, Bread_Sliced_8 are in/on CounterTop
  PepperShaker_0, Faucet, Cup_0, Egg_0, Spatula_0, SoapBottle are in/on Sink"""  
  ...
512: 2023/05/02 12:14:31 - 12:14:34: """Goal: Place(CounterTop)
  Visual observation: Bowl_1 [filled], Cabinet_1, Cabinet_3, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, agent hand, Fork, Cup_0 [filled]
  Bread_Sliced_5, ButterKnife_0, Knife, Bread_Sliced_2, Bread_Sliced_3, Bowl_0, Potato_1, Bread_Sliced_6, Bread_Sliced_7, Bread_Sliced_4, DishSponge_0, Bowl_1, Bread_Sliced_8, HousePlant, Bread_Sliced_1 are in/on CounterTop
  Spatula_0, Cup_0, Faucet are in/on Sink
  Fork is inside agent hand"""  
  ...
513: 2023/05/02 12:14:35 - 12:14:48: """Goal: Pickup(ButterKnife_2)
  Visual observation: PepperShaker_1, ButterKnife_2, Egg_2, Potato_0, Fridge, Pan_0, Drawer_2, Drawer_3, Drawer_4, SideTable, Drawer_5, Drawer_6, Drawer_7, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Bowl_1 [filled], Floor, Knife, Bowl_0 [filled], Fork, Sink, Cup_0 [filled], ButterKnife_0
  Bread_Sliced_5, Bowl_1, Bread_Sliced_2, Bread_Sliced_3, Potato_1, Bread_Sliced_6, Bread_Sliced_7, Bread_Sliced_4, Knife, Fork, ButterKnife_0, Bread_Sliced_8, Bread_Sliced_1, Bowl_0 are in/on CounterTop
  Drawer_6, Fridge, SideTable, Drawer_5 are in/on Floor
  Potato_0, Pan_0, PepperShaker_1, ButterKnife_2, Egg_2 are in/on SideTable
  Cup_0 is in/on Sink"""  
  ...
514: 2023/05/02 12:14:51 - 12:15:02: """Goal: Place(Sink_Basin)
  Visual observation: ButterKnife_2, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, agent hand, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Knife, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  ButterKnife_2 is inside agent hand"""  
  ...
515: 2023/05/02 12:15:04 - 12:15:04: """Goal: ToggleOn(Faucet)
  Visual observation: ButterKnife_2, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Bowl_0, DishSponge_0, Knife, Fork, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  ButterKnife_2 is in/on Sink_Basin"""  
  ...
516: 2023/05/02 12:15:07 - 12:15:07: """Goal: ToggleOff(Faucet)
  Visual observation: ButterKnife_2, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Bowl_0, DishSponge_0, Knife, Fork, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  ButterKnife_2 is in/on Sink_Basin"""  
  ...
517: 2023/05/02 12:15:10 - 12:15:10: """Goal: Pickup(ButterKnife_2)
  Visual observation: ButterKnife_2, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, Potato_1, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Bowl_0, DishSponge_0, Knife, Fork, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  ButterKnife_2 is in/on Sink_Basin"""  
  ...
518: 2023/05/02 12:15:11 - 12:15:15: """Goal: Place(CounterTop)
  Visual observation: ButterKnife_2, Bowl_1 [filled], Cabinet_1, Cabinet_3, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, agent hand, Potato_1, Knife, Fork, Cup_0 [filled]
  Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_5, Potato_1, ButterKnife_0, Bowl_1, Knife, Fork, Bowl_0, Bread_Sliced_3, Bread_Sliced_2, HousePlant, Bread_Sliced_1, Bread_Sliced_6, Bread_Sliced_4, DishSponge_0 are in/on CounterTop
  Faucet, Cup_0, Spatula_0 are in/on Sink
  ButterKnife_2 is inside agent hand"""  
  ...
519: 2023/05/02 12:15:17 - 12:15:31: """Goal: Pickup(Spatula_1)
  Visual observation: Bread__0, Tomato_1_Sliced_4, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, Spatula_1, WineBottle, Plate_0, CoffeeMachine [toggled], SideTable, Stool, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Bowl_1 [filled], Floor, Knife, Bowl_0 [filled], Fork, Sink, Cup_0 [filled], ButterKnife_0
  Bowl_1, ButterKnife_0, Plate_0, Bread_Sliced_3, WineBottle, Tomato_1_Sliced_0, Bread_Sliced_1, Bread_Sliced_7, Tomato_1_Sliced_1, Bread_Sliced_4, Bread__0, Bread_Sliced_5, Bread_Sliced_2, Tomato_1_Sliced_4, Bowl_0, Knife, Tomato_1_Sliced_2, Bread_Sliced_8, Potato_1, Bread_Sliced_6, Fork, ButterKnife_2, CoffeeMachine are in/on CounterTop
  Cup_0 is in/on Sink
  SideTable, Stool are in/on Floor
  Spatula_1 is in/on Stool"""  
  ...
520: 2023/05/02 12:15:32 - 12:15:39: """Goal: Place(Sink)
  Visual observation: Spatula_1, Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, agent hand, Potato_1, Bowl_1 [filled], Knife, Fork
  Bread_Sliced_8, Potato_1, Knife, ButterKnife_0, HousePlant, Bread_Sliced_2, ButterKnife_2, Bowl_1, Bread_Sliced_3, Bread_Sliced_6, Bread_Sliced_1, Bowl_0, Bread_Sliced_7, DishSponge_0, Fork, Bread_Sliced_5, Bread_Sliced_4, Pot are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Spatula_0, Faucet, PepperShaker_0 are in/on Sink
  Spatula_1 is inside agent hand"""  
  ...
521: 2023/05/02 12:15:43 - 12:15:43: """Goal: Pickup(Spatula_1)
  Visual observation: Spatula_1, Cabinet_0, Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Bowl_1 [filled], Knife, Fork
  Bread_Sliced_8, Bowl_1, Fork, ButterKnife_0, Potato_1, HousePlant, Bread_Sliced_2, ButterKnife_2, Bread_Sliced_3, Knife, Bread_Sliced_6, Bread_Sliced_1, Bowl_0, Bread_Sliced_7, DishSponge_0, Bread_Sliced_5, Bread_Sliced_4, Pot are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Spatula_0, Faucet, PepperShaker_0, Spatula_1 are in/on Sink"""  
  ...
522: 2023/05/02 12:15:45 - 12:15:48: """Goal: Place(Sink_Basin)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, agent hand, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0, Spatula_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Knife, Bread_Sliced_7, Bowl_0, DishSponge_0, Fork, Potato_1, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Spatula_1 is inside agent hand"""  
  ...
523: 2023/05/02 12:15:50 - 12:15:54: """Goal: Pickup(Spatula_0)
  Visual observation: Spatula_1, Cabinet_0, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Bowl_1 [filled], Knife, Bowl_0 [filled], Fork
  Bread_Sliced_6, ButterKnife_0, DishSponge_0, Bowl_1, Knife, Bread_Sliced_7, Bread_Sliced_1, Fork, ButterKnife_2, Potato_1, Bread_Sliced_5, HousePlant, Bread_Sliced_4, Bread_Sliced_3, Pot, Bread_Sliced_2, Bowl_0, Bread_Sliced_8 are in/on CounterTop
  Spatula_1 is in/on Sink_Basin
  PepperShaker_0, Faucet, Cup_0, Egg_0, Spatula_0, SoapBottle are in/on Sink"""  
  ...
524: 2023/05/02 12:15:55 - 12:15:59: """Goal: Place(Sink_Basin)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork, agent hand
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Knife, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Spatula_0 is inside agent hand
  Spatula_1 is in/on Sink_Basin"""  
  ...
525: 2023/05/02 12:16:02 - 12:16:02: """Goal: ToggleOn(Faucet)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Knife, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Spatula_0, Spatula_1 are in/on Sink_Basin"""  
  ...
526: 2023/05/02 12:16:06 - 12:16:06: """Goal: ToggleOff(Faucet)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Knife, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Spatula_0, Spatula_1 are in/on Sink_Basin"""  
  ...
527: 2023/05/02 12:16:08 - 12:16:08: """Goal: Pickup(Spatula_1)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Knife, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Spatula_0, Spatula_1 are in/on Sink_Basin"""  
  ...
528: 2023/05/02 12:16:11 - 12:16:11: """Goal: Place(CounterTop)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, agent hand, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Knife, Bread_Sliced_7, Bowl_0, DishSponge_0, Fork, Potato_1, Bread_Sliced_8, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Spatula_1 is inside agent hand
  Spatula_0 is in/on Sink_Basin"""  
  ...
529: 2023/05/02 12:16:14 - 12:16:14: """Goal: Pickup(Spatula_0)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Knife, Bread_Sliced_8, Spatula_1, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Spatula_0 is in/on Sink_Basin"""  
  ...
530: 2023/05/02 12:16:17 - 12:16:17: """Goal: Place(CounterTop)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork, agent hand
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Knife, Bread_Sliced_8, Spatula_1, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Spatula_0 is inside agent hand"""  
  ...
531: 2023/05/02 12:16:23 - 12:17:16: """Goal: Pickup(Knife)
  Visual observation: Bread__0, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, LightSwitch [toggled], WineBottle, Plate_0, CoffeeMachine [toggled], Stool, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Spatula_1, Potato_1, Bowl_1 [filled], Floor, Knife, Bowl_0 [filled], Fork, Sink, Cup_0 [filled], Spatula_0, ButterKnife_0
  Potato_1, Bowl_1, WineBottle, Bread_Sliced_3, Tomato_1_Sliced_1, Bread_Sliced_1, ButterKnife_0, Bread_Sliced_7, Tomato_1_Sliced_2, Bread_Sliced_4, Bread__0, Bread_Sliced_5, Fork, Tomato_1_Sliced_0, Bread_Sliced_2, Tomato_1_Sliced_4, Knife, CoffeeMachine, Spatula_0, Tomato_1_Sliced_3, Bread_Sliced_8, Spatula_1, Bread_Sliced_6, Bowl_0, ButterKnife_2, Plate_0 are in/on CounterTop
  Cup_0 is in/on Sink
  Stool is in/on Floor"""  
  ...
532: 2023/05/02 12:17:18 - 12:17:26: """Goal: Place(Sink_Basin)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, agent hand, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Fork, Bread_Sliced_8, Spatula_0, Spatula_1, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Knife is inside agent hand"""  
  ...
533: 2023/05/02 12:17:29 - 12:17:29: """Goal: ToggleOn(Faucet)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Bread_Sliced_8, Spatula_0, Spatula_1, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Knife is in/on Sink_Basin"""  
  ...
534: 2023/05/02 12:17:32 - 12:17:32: """Goal: ToggleOff(Faucet)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Bread_Sliced_8, Spatula_0, Spatula_1, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Knife is in/on Sink_Basin"""  
  ...
535: 2023/05/02 12:17:37 - 12:17:37: """Goal: Pickup(Knife)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Potato_1, Knife, Fork
  SoapBottle, Cup_0, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Fork, Bread_Sliced_7, Bowl_0, DishSponge_0, Potato_1, Bread_Sliced_8, Spatula_0, Spatula_1, Bowl_1, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  Knife is in/on Sink_Basin"""  
  ...
536: 2023/05/02 12:17:39 - 12:17:41: """Goal: Place(CounterTop)
  Visual observation: ButterKnife_2, Spatula_1, Bowl_1 [filled], Cabinet_1, Cabinet_3, Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, agent hand, Knife, Fork, Cup_0 [filled]
  Bread_Sliced_3, Bowl_0, Spatula_0, Bread_Sliced_2, HousePlant, Bread_Sliced_1, Bread_Sliced_7, Bread_Sliced_5, ButterKnife_0, Fork, Bread_Sliced_8, Bread_Sliced_6, ButterKnife_2, Spatula_1, Potato_1, Bowl_1, DishSponge_0, Bread_Sliced_4 are in/on CounterTop
  Faucet, Cup_0 are in/on Sink
  Knife is inside agent hand"""  
  ...
537: 2023/05/02 12:17:45 - 12:18:00: """Goal: Open(Cabinet_3)
  Visual observation: ButterKnife_2, Spatula_1, Bowl_1 [filled], Cabinet_1, Cabinet_3, Drawer_0, Sink, Bowl_0 [filled], HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Potato_1, Knife, Fork, Cup_0 [filled]
  Bread_Sliced_6, Bread_Sliced_3, ButterKnife_2, Spatula_1, Bowl_1, Bread_Sliced_7, HousePlant, Spatula_0, Bread_Sliced_1, Potato_1, Fork, ButterKnife_0, Knife, Bowl_0, Bread_Sliced_4, Bread_Sliced_2, Bread_Sliced_8, Bread_Sliced_5 are in/on CounterTop
  Cup_0 is in/on Sink"""  
  ...
...
544: 2023/05/02 12:18:49 - 12:18:55: """Goal: Close(Cabinet_1)
  Visual observation: Plate_1 [dirty], ButterKnife_2, Spatula_1, Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, agent hand, PaperTowelRoll_1, Potato_1, Floor, Knife, Fork, Cup_0 [filled]
  Cabinet_1 is in/on Floor
  Bread_Sliced_3, Bowl_0, Spatula_0, Bread_Sliced_2, DishSponge_0, HousePlant, Bread_Sliced_1, Fork, Bread_Sliced_7, Bread_Sliced_5, ButterKnife_0, Bowl_1, Bread_Sliced_8, Knife, Bread_Sliced_6, ButterKnife_2, Spatula_1, PaperTowelRoll_1, Potato_1, Bread_Sliced_4 are in/on CounterTop
  Faucet, Cup_0 are in/on Sink
  Plate_1 is inside agent hand"""  
  ...
545: 2023/05/02 12:18:57 - 12:19:12: """Goal: Place(Sink_Basin)
  Visual observation: Plate_1 [dirty], Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, agent hand, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0
  Bread_Sliced_6, Knife, ButterKnife_0, DishSponge_0, PaperTowelRoll_1, Spatula_1, Bread_Sliced_7, HousePlant, Bread_Sliced_1, Bowl_1, ButterKnife_2, Bread_Sliced_5, Bowl_0, Fork, Bread_Sliced_4, Spatula_0, Bread_Sliced_3, Bread_Sliced_2, Potato_1, Pot, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, PepperShaker_0, Egg_0, Cup_0, Faucet are in/on Sink
  Plate_1 is inside agent hand"""  
  ...
546: 2023/05/02 12:19:16 - 12:19:16: """Goal: ToggleOn(Faucet)
  Visual observation: Plate_1 [dirty], Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0
  Bowl_0, Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, Fork, Spatula_0, Bread_Sliced_3, Bread_Sliced_4, Potato_1, Bread_Sliced_7, Pot, Knife, DishSponge_0, PaperTowelRoll_1, Bowl_1, Spatula_1, Bread_Sliced_8, HousePlant, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Faucet, PepperShaker_0 are in/on Sink
  Plate_1 is in/on Sink_Basin
  Speech:
  2023-05-02 12:19:16.158851: behind you there are tableware. rinse with water"""  
  ...
547: 2023/05/02 12:19:20 - 12:19:20: """Goal: Pickup(Cup_0)
  Visual observation: Plate_1, Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0
  Bowl_0, Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, Fork, Spatula_0, Bread_Sliced_3, Bread_Sliced_4, Potato_1, Bread_Sliced_7, Pot, Knife, DishSponge_0, PaperTowelRoll_1, Bowl_1, Spatula_1, Bread_Sliced_8, HousePlant, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Faucet, PepperShaker_0 are in/on Sink
  Plate_1 is in/on Sink_Basin"""  
  ...
548: 2023/05/02 12:19:26 - 12:19:29: """Goal: ToggleOff(Faucet)
  Visual observation: Plate_1, Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, agent hand, Spatula_0
  Bowl_0, Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, Fork, Bread_Sliced_3, Bread_Sliced_4, Potato_1, Bread_Sliced_7, Pot, Knife, DishSponge_0, PaperTowelRoll_1, Bowl_1, Spatula_1, Spatula_0, Bread_Sliced_8, HousePlant, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  SoapBottle, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Cup_0 is inside agent hand
  Plate_1 is in/on Sink_Basin"""  
  ...
549: 2023/05/02 12:19:31 - 12:19:31: """Goal: Place(Sink)
  Visual observation: Plate_1, Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, agent hand, Spatula_0
  Bowl_0, Bread_Sliced_5, ButterKnife_2, Bread_Sliced_6, Fork, Bread_Sliced_3, Bread_Sliced_4, Potato_1, Bread_Sliced_7, Pot, Knife, DishSponge_0, PaperTowelRoll_1, Bowl_1, Spatula_1, Spatula_0, Bread_Sliced_8, HousePlant, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  SoapBottle, Egg_0, Faucet, PepperShaker_0 are in/on Sink
  Cup_0 is inside agent hand
  Plate_1 is in/on Sink_Basin"""  
  ...
550: 2023/05/02 12:19:34 - 12:19:45: """Goal: Pickup(Plate_0)
  Visual observation: Tomato_1_Sliced_4, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, LightSwitch [toggled], WineBottle, Plate_0, CoffeeMachine [toggled], SideTable, Stool, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Sink_Basin, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Floor, Knife, Bowl_0 [filled], Fork, Sink, Cup_0 [filled], Spatula_0, ButterKnife_0
  Bread_Sliced_1, Potato_1, Tomato_1_Sliced_1, Bread_Sliced_7, Tomato_1_Sliced_2, Bowl_1, Bread_Sliced_5, ButterKnife_2, PaperTowelRoll_1, Spatula_0, ButterKnife_0, Spatula_1, Bread_Sliced_8, Bread_Sliced_2, Plate_0, CoffeeMachine, Fork, Bread_Sliced_6, Bread_Sliced_4, Tomato_1_Sliced_0, Bread_Sliced_3, Bowl_0, Tomato_1_Sliced_4, Knife, WineBottle are in/on CounterTop
  Stool, SideTable are in/on Floor
  Plate_1 is in/on Sink_Basin
  Cup_0 is in/on Sink"""  
  ...
551: 2023/05/02 12:19:47 - 12:19:53: """Goal: Place(CounterTop)
  Visual observation: Plate_1, Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, ButterKnife_0, Plate_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Sink_Basin, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0, agent hand
  Bowl_0, Bread_Sliced_5, Bread_Sliced_6, Knife, Fork, Bread_Sliced_3, Bread_Sliced_4, Spatula_1, Bread_Sliced_7, Pot, Bowl_1, ButterKnife_0, DishSponge_0, ButterKnife_2, Potato_1, PaperTowelRoll_1, Spatula_0, Bread_Sliced_8, HousePlant, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Faucet, PepperShaker_0 are in/on Sink
  Plate_0 is inside agent hand
  Plate_1 is in/on Sink_Basin"""  
  ...
552: 2023/05/02 12:19:56 - 12:19:56: """Goal: Pickup(Plate_1)
  Visual observation: Plate_1, Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, Plate_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0
  Bread_Sliced_8, Spatula_1, Bowl_1, Plate_0, PaperTowelRoll_1, HousePlant, Bread_Sliced_2, ButterKnife_2, Potato_1, Bread_Sliced_3, Spatula_0, Bread_Sliced_6, Bread_Sliced_1, ButterKnife_0, Bowl_0, Bread_Sliced_7, DishSponge_0, Knife, Bread_Sliced_5, Fork, Bread_Sliced_4, Pot are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Faucet, PepperShaker_0 are in/on Sink
  Plate_1 is in/on Sink_Basin"""  
  ...
553: 2023/05/02 12:19:57 - 12:20:00: """Goal: Place(CounterTop)
  Visual observation: Plate_1, ButterKnife_2, PaperTowelRoll_1, Egg_1, Cabinet_1 [open], Cabinet_3 [open], Bowl_0 [filled], Lettuce_0, HousePlant, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, agent hand, Spatula_1, Potato_1, Bowl_1 [filled], Floor, Knife, Fork, Sink, Cup_0 [filled], Spatula_0, ButterKnife_0, Plate_0
  Bowl_0, Spatula_1, Plate_0, Bread_Sliced_5, Bread_Sliced_3, Bread_Sliced_2, Spatula_0, ButterKnife_0, Knife, Bread_Sliced_6, ButterKnife_2, Bread_Sliced_4, Fork, HousePlant, PaperTowelRoll_1, Bowl_1, Potato_1, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_1 are in/on CounterTop
  Egg_1, Lettuce_0 are in/on Cabinet_3
  Cabinet_3 is in/on Floor
  Cup_0 is in/on Sink
  Plate_1 is inside agent hand"""  
  ...
554: 2023/05/02 12:20:01 - 12:20:08: """Goal: Pickup(Plate_0)
  Visual observation: Cabinet_0, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, Plate_0, PepperShaker_0, Toaster [toggled], CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Bowl_0 [filled], Fork, Spatula_0, ButterKnife_0
  Bread_Sliced_6, Knife, Pot, Bowl_0, Bread_Sliced_3, Spatula_1, Spatula_0, Bread_Sliced_7, Potato_1, Plate_0, Bowl_1, Bread_Sliced_1, Plate_1, Toaster, PaperTowelRoll_1, ButterKnife_2, Fork, Bread_Sliced_4, Bread_Sliced_2, ButterKnife_0, Bread_Sliced_8, Bread_Sliced_5 are in/on CounterTop
  PepperShaker_0, SoapBottle, Cup_0, Faucet, Egg_0 are in/on Sink"""  
  ...
555: 2023/05/02 12:20:10 - 12:20:19: """Goal: Place(Sink_Basin)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, ButterKnife_0, Plate_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0, agent hand
  Bread_Sliced_6, Knife, DishSponge_0, PaperTowelRoll_1, Spatula_1, Bread_Sliced_7, ButterKnife_0, Bread_Sliced_1, Bowl_1, Plate_1, ButterKnife_2, Bread_Sliced_5, Fork, Bread_Sliced_4, Spatula_0, HousePlant, Bread_Sliced_3, Pot, Bread_Sliced_2, Potato_1, Bowl_0, Bread_Sliced_8 are in/on CounterTop
  Plate_0 is inside agent hand
  PepperShaker_0, Faucet, SoapBottle, Cup_0, Egg_0 are in/on Sink"""  
  ...
556: 2023/05/02 12:20:25 - 12:20:25: """Goal: ToggleOn(Faucet)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, Plate_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0
  Bread_Sliced_5, Plate_1, Bread_Sliced_6, Knife, Fork, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Pot, Spatula_1, Bread_Sliced_7, Bowl_0, Bowl_1, ButterKnife_0, DishSponge_0, ButterKnife_2, Potato_1, PaperTowelRoll_1, Spatula_0, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  PepperShaker_0, Faucet, SoapBottle, Cup_0, Egg_0 are in/on Sink
  Plate_0 is in/on Sink_Basin"""  
  ...
557: 2023/05/02 12:20:28 - 12:20:28: """Goal: ToggleOff(Faucet)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, Plate_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0
  Bread_Sliced_5, Plate_1, Bread_Sliced_6, Knife, Fork, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Pot, Spatula_1, Bread_Sliced_7, Bowl_0, Bowl_1, ButterKnife_0, DishSponge_0, ButterKnife_2, Potato_1, PaperTowelRoll_1, Spatula_0, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  PepperShaker_0, Faucet, SoapBottle, Cup_0, Egg_0 are in/on Sink
  Plate_0 is in/on Sink_Basin"""  
  ...
558: 2023/05/02 12:20:32 - 12:20:32: """Goal: Pickup(Plate_0)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, Plate_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Spatula_0
  Bread_Sliced_5, Plate_1, Bread_Sliced_6, Knife, Fork, HousePlant, Bread_Sliced_3, Bread_Sliced_4, Pot, Spatula_1, Bread_Sliced_7, Bowl_0, Bowl_1, ButterKnife_0, DishSponge_0, ButterKnife_2, Potato_1, PaperTowelRoll_1, Spatula_0, Bread_Sliced_8, Bread_Sliced_1, Bread_Sliced_2 are in/on CounterTop
  PepperShaker_0, Faucet, SoapBottle, Cup_0, Egg_0 are in/on Sink
  Plate_0 is in/on Sink_Basin"""  
  ...
559: 2023/05/02 12:20:33 - 12:20:36: """Goal: Place(CounterTop)
  Visual observation: Plate_1, ButterKnife_2, Spatula_1, Bowl_1 [filled], Egg_1, Cabinet_1 [open], Cabinet_3 [open], Drawer_0, Bowl_0 [filled], Lettuce_0, HousePlant, Plate_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, PaperTowelRoll_1, Potato_1, Floor, Knife, Fork, Sink, Cup_0 [filled], Spatula_0, ButterKnife_0, agent hand
  Bread_Sliced_6, Spatula_0, Bread_Sliced_3, Plate_1, ButterKnife_2, Knife, Spatula_1, Bread_Sliced_7, Bowl_0, Fork, Bread_Sliced_1, HousePlant, PaperTowelRoll_1, Potato_1, ButterKnife_0, Bread_Sliced_4, Bread_Sliced_2, Bread_Sliced_8, Bowl_1, Bread_Sliced_5 are in/on CounterTop
  Lettuce_0, Egg_1 are in/on Cabinet_3
  Cup_0 is in/on Sink
  Cabinet_3 is in/on Floor
  Plate_0 is inside agent hand"""  
  ...
...
561: 2023/05/02 12:21:01 - 12:21:35: """Goal: Place(CounterTop)
  Visual observation: Plate_1, PaperTowelRoll_1, Egg_1, Cabinet_1 [open], Cabinet_3 [open], GarbageCan, Pan_0, Plate_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Spatula_1, Potato_1, Bowl_1 [filled], Floor, Knife, Bowl_0 [filled], Fork, Sink, Cup_0 [filled], agent hand, Spatula_0, ButterKnife_0
  Bread_Sliced_3, Bread_Sliced_8, Bowl_1, Bread_Sliced_7, Bread_Sliced_6, Bowl_0, ButterKnife_0, Plate_0, ButterKnife_2, Knife, Potato_1, Bread_Sliced_4, Bread_Sliced_1, Bread_Sliced_2, Spatula_0, Bread_Sliced_5, Spatula_1, Plate_1, PaperTowelRoll_1, Fork are in/on CounterTop
  Pan_0 is inside agent hand
  Cup_0 is in/on Sink
  Cabinet_3, GarbageCan are in/on Floor
  Egg_1 is in/on Cabinet_3"""  
  ...
...
563: 2023/05/02 12:22:00 - 12:22:08: """Goal: Place(Sink)
  Visual observation: Cup_1 [dirty, filled], Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, agent hand, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, Plate_0
  Bowl_0, Plate_0, Bread_Sliced_5, Plate_1, Bread_Sliced_6, Bowl_1, Knife, Bread_Sliced_3, Bread_Sliced_4, Spatula_1, Pan_0, Bread_Sliced_7, Pot, Potato_1, DishSponge_0, ButterKnife_2, PaperTowelRoll_1, Fork, Bread_Sliced_8, HousePlant, Spatula_0, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Faucet, PepperShaker_0 are in/on Sink
  Cup_1 is inside agent hand"""  
  ...
564: 2023/05/02 12:22:12 - 12:22:12: """Goal: Pickup(Cup_1)
  Visual observation: Cup_1 [dirty, filled], Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, Plate_0
  Bowl_0, Bread_Sliced_5, Plate_1, Bread_Sliced_6, Knife, Fork, Bread_Sliced_3, Bread_Sliced_4, Spatula_1, Spatula_0, Bread_Sliced_7, Pot, Bowl_1, DishSponge_0, ButterKnife_2, Potato_1, PaperTowelRoll_1, Pan_0, Bread_Sliced_8, HousePlant, Plate_0, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Faucet, Cup_1, PepperShaker_0 are in/on Sink"""  
  ...
565: 2023/05/02 12:22:15 - 12:22:15: """Goal: Place(Sink)
  Visual observation: Cup_1 [dirty, filled], Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, agent hand, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, Plate_0
  Bowl_0, Plate_0, Bread_Sliced_5, Plate_1, Bread_Sliced_6, Bowl_1, Knife, Bread_Sliced_3, Bread_Sliced_4, Spatula_1, Pan_0, Bread_Sliced_7, Pot, Potato_1, DishSponge_0, ButterKnife_2, PaperTowelRoll_1, Fork, Bread_Sliced_8, HousePlant, Spatula_0, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Faucet, PepperShaker_0 are in/on Sink
  Cup_1 is inside agent hand"""  
  ...
566: 2023/05/02 12:22:23 - 12:22:23: """Goal: Pickup(Cup_1)
  Visual observation: Cup_1 [dirty, filled], Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, Plate_0
  Bowl_0, Bread_Sliced_5, Plate_1, Bread_Sliced_6, Knife, Fork, Bread_Sliced_3, Bread_Sliced_4, Spatula_1, Spatula_0, Bread_Sliced_7, Pot, Bowl_1, DishSponge_0, ButterKnife_2, Potato_1, PaperTowelRoll_1, Pan_0, Bread_Sliced_8, HousePlant, Plate_0, Bread_Sliced_1, Bread_Sliced_2, ButterKnife_0 are in/on CounterTop
  SoapBottle, Egg_0, Cup_0, Faucet, Cup_1, PepperShaker_0 are in/on Sink"""  
  ...
567: 2023/05/02 12:22:24 - 12:22:30: """Goal: Place(Sink)
  Visual observation: Spatula_1, Cup_1 [dirty, filled], Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, agent hand, Potato_1, Knife, Fork, Pan_0, Plate_0
  Bread_Sliced_8, PaperTowelRoll_1, Spatula_0, Potato_1, ButterKnife_0, ButterKnife_2, HousePlant, Bread_Sliced_2, Plate_1, Spatula_1, Bread_Sliced_3, Bowl_1, Pan_0, Bread_Sliced_6, Bread_Sliced_1, Bowl_0, Bread_Sliced_7, DishSponge_0, Knife, Bread_Sliced_5, Fork, Bread_Sliced_4, Plate_0 are in/on CounterTop
  Faucet, PepperShaker_0, SoapBottle, Egg_0, Cup_0 are in/on Sink
  Cup_1 is inside agent hand"""  
  ...
568: 2023/05/02 12:22:33 - 12:22:33: """Goal: Pickup(Spatula_1)
  Visual observation: Spatula_1, Cup_1 [dirty, filled], Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, ButterKnife_0, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Potato_1, Knife, Fork, Pan_0, Plate_0
  Bread_Sliced_8, PaperTowelRoll_1, Spatula_0, Knife, ButterKnife_0, ButterKnife_2, HousePlant, Bread_Sliced_2, Plate_1, Spatula_1, Potato_1, Bread_Sliced_3, Bowl_1, Plate_0, Bread_Sliced_6, Bread_Sliced_1, Bowl_0, Bread_Sliced_7, DishSponge_0, Fork, Bread_Sliced_5, Pan_0, Bread_Sliced_4 are in/on CounterTop
  Faucet, PepperShaker_0, Cup_1, SoapBottle, Egg_0, Cup_0 are in/on Sink"""  
  ...
569: 2023/05/02 12:22:35 - 12:22:39: """Goal: Place(CounterTop)
  Visual observation: Plate_1, PaperTowelRoll_1, Egg_1, Cabinet_1 [open], Cabinet_3 [open], GarbageCan, Pan_0, Lettuce_0, ButterKnife_0, Plate_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, ButterKnife_2, Spatula_1, Sink, Cup_1 [dirty, filled], Potato_1, Bowl_1 [filled], Floor, Knife, Bowl_0 [filled], Fork, Cup_0 [filled], Spatula_0, agent hand
  Bread_Sliced_1, Bowl_1, Spatula_0, Bread_Sliced_7, PaperTowelRoll_1, Bowl_0, Bread_Sliced_5, Knife, Spatula_1, Plate_0, Potato_1, Bread_Sliced_8, Bread_Sliced_2, Pan_0, ButterKnife_2, Bread_Sliced_6, Bread_Sliced_4, Bread_Sliced_3, Fork, Plate_1 are in/on CounterTop
  ButterKnife_0 is inside agent hand
  GarbageCan, Cabinet_3 are in/on Floor
  Lettuce_0, Egg_1 are in/on Cabinet_3
  Cup_1, Cup_0 are in/on Sink"""  
  ...
570: 2023/05/02 12:22:40 - 12:22:47: """Goal: Pickup(Cup_1)
  Visual observation: Cup_1 [dirty, filled], Cabinet_0, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Bowl_0 [filled], Fork, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  Bread_Sliced_8, Bread_Sliced_7, Bowl_1, Potato_1, Bread_Sliced_5, ButterKnife_2, Bowl_0, ButterKnife_0, PaperTowelRoll_1, Spatula_1, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Pan_0, HousePlant, Spatula_0, Plate_1, Plate_0, Bread_Sliced_6, Pot, Bread_Sliced_4, Knife, DishSponge_0, Fork are in/on CounterTop
  Cup_1, PepperShaker_0, Faucet, Cup_0, Egg_0, SoapBottle are in/on Sink
  Speech:
  2023-05-02 12:22:46.133527: tableware surfaces"""  
  ...
571: 2023/05/02 12:22:50 - 12:22:55: """Goal: Place(Sink)
  Visual observation: Cup_1 [dirty, filled], Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, agent hand, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  Bread_Sliced_6, Bowl_1, DishSponge_0, PaperTowelRoll_1, Spatula_1, Pan_0, Bread_Sliced_7, HousePlant, Bread_Sliced_1, Potato_1, ButterKnife_0, Plate_1, Plate_0, ButterKnife_2, Bread_Sliced_5, Bowl_0, Knife, Bread_Sliced_4, Fork, Bread_Sliced_3, Bread_Sliced_2, Spatula_0, Pot, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, PepperShaker_0, Egg_0, Cup_0, Faucet are in/on Sink
  Cup_1 is inside agent hand"""  
  ...
572: 2023/05/02 12:22:59 - 12:22:59: """Goal: Pickup(Cup_1)
  Visual observation: Cup_1 [dirty, filled], Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  Bread_Sliced_6, Knife, DishSponge_0, PaperTowelRoll_1, Spatula_1, Spatula_0, Bread_Sliced_7, HousePlant, Bread_Sliced_1, Bowl_1, Plate_0, Plate_1, ButterKnife_2, Bread_Sliced_5, Bowl_0, Fork, Bread_Sliced_4, Pan_0, Bread_Sliced_3, Bread_Sliced_2, Potato_1, Pot, ButterKnife_0, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, PepperShaker_0, Egg_0, Cup_0, Faucet, Cup_1 are in/on Sink"""  
  ...
573: 2023/05/02 12:23:01 - 12:23:04: """Goal: Place(Sink_Basin)
  Visual observation: ButterKnife_2, Spatula_1, Cup_1 [dirty, filled], Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], HousePlant, Spatula_0, Sink_Basin, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, PaperTowelRoll_1, agent hand, Potato_1, Knife, Fork, Pan_0, ButterKnife_0, Plate_0
  Bread_Sliced_6, Pan_0, Spatula_0, Bowl_1, DishSponge_0, Potato_1, Bread_Sliced_7, HousePlant, ButterKnife_2, Spatula_1, Bread_Sliced_1, Fork, Plate_1, Bowl_0, PaperTowelRoll_1, Bread_Sliced_5, ButterKnife_0, Bread_Sliced_4, Plate_0, Bread_Sliced_3, Bread_Sliced_2, Knife, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, Cup_0, Faucet are in/on Sink
  Cup_1 is inside agent hand"""  
  ...
574: 2023/05/02 12:23:06 - 12:23:08: """Goal: ToggleOn(Faucet)
  Visual observation: Spatula_1, Cup_1 [dirty, filled], Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Potato_1, Knife, Fork, Pan_0, ButterKnife_0, Plate_0
  Bowl_0, Bread_Sliced_5, Plate_1, Bread_Sliced_6, Pan_0, ButterKnife_0, Bread_Sliced_3, Bread_Sliced_4, Potato_1, Bread_Sliced_7, Fork, Spatula_0, DishSponge_0, ButterKnife_2, Knife, PaperTowelRoll_1, Plate_0, Bread_Sliced_8, HousePlant, Spatula_1, Bread_Sliced_1, Bread_Sliced_2, Bowl_1 are in/on CounterTop
  Faucet, PepperShaker_0, SoapBottle, Egg_0, Cup_0 are in/on Sink
  Cup_1 is in/on Sink_Basin"""  
  ...
575: 2023/05/02 12:23:11 - 12:23:11: """Goal: ToggleOff(Faucet)
  Visual observation: Spatula_1, Cup_1 [filled], Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Potato_1, Knife, Fork, Pan_0, ButterKnife_0, Plate_0
  Bowl_0, Bread_Sliced_5, Plate_1, Bread_Sliced_6, Pan_0, ButterKnife_0, Bread_Sliced_3, Bread_Sliced_4, Potato_1, Bread_Sliced_7, Fork, Spatula_0, DishSponge_0, ButterKnife_2, Knife, PaperTowelRoll_1, Plate_0, Bread_Sliced_8, HousePlant, Spatula_1, Bread_Sliced_1, Bread_Sliced_2, Bowl_1 are in/on CounterTop
  Faucet, PepperShaker_0, SoapBottle, Egg_0, Cup_0 are in/on Sink
  Cup_1 is in/on Sink_Basin"""  
  ...
576: 2023/05/02 12:23:14 - 12:23:14: """Goal: Pickup(Cup_1)
  Visual observation: Spatula_1, Cup_1 [filled], Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Potato_1, Knife, Fork, Pan_0, ButterKnife_0, Plate_0
  Bowl_0, Bread_Sliced_5, Plate_1, Bread_Sliced_6, Pan_0, ButterKnife_0, Bread_Sliced_3, Bread_Sliced_4, Potato_1, Bread_Sliced_7, Fork, Spatula_0, DishSponge_0, ButterKnife_2, Knife, PaperTowelRoll_1, Plate_0, Bread_Sliced_8, HousePlant, Spatula_1, Bread_Sliced_1, Bread_Sliced_2, Bowl_1 are in/on CounterTop
  Faucet, PepperShaker_0, SoapBottle, Egg_0, Cup_0 are in/on Sink
  Cup_1 is in/on Sink_Basin"""  
  ...
577: 2023/05/02 12:23:16 - 12:23:19: """Goal: Pour(Sink_Basin)
  Visual observation: ButterKnife_2, Spatula_1, Cup_1 [filled], Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], HousePlant, Spatula_0, Sink_Basin, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, PaperTowelRoll_1, agent hand, Potato_1, Knife, Fork, Pan_0, ButterKnife_0, Plate_0
  Bread_Sliced_6, Pan_0, Spatula_0, Bowl_1, DishSponge_0, Potato_1, Bread_Sliced_7, HousePlant, ButterKnife_2, Spatula_1, Bread_Sliced_1, Fork, Plate_1, Bowl_0, PaperTowelRoll_1, Bread_Sliced_5, ButterKnife_0, Bread_Sliced_4, Plate_0, Bread_Sliced_3, Bread_Sliced_2, Knife, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, Cup_0, Faucet are in/on Sink
  Cup_1 is inside agent hand"""  
  ...
578: 2023/05/02 12:23:21 - 12:23:26: """Goal: Place(CounterTop)
  Visual observation: Plate_1, ButterKnife_2, Spatula_1, Cup_1, Bowl_1 [filled], Egg_1, Cabinet_1 [open], Cabinet_3 [open], Drawer_0, Sink, Bowl_0 [filled], HousePlant, Plate_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, PaperTowelRoll_1, agent hand, Potato_1, Floor, Knife, Fork, Cup_0 [filled], Pan_0, Spatula_0, ButterKnife_0
  Bread_Sliced_5, HousePlant, Bread_Sliced_2, Bowl_0, Pan_0, Bread_Sliced_3, PaperTowelRoll_1, Bowl_1, Bread_Sliced_6, ButterKnife_0, Bread_Sliced_7, Bread_Sliced_4, Plate_0, Plate_1, Fork, Spatula_0, Potato_1, Bread_Sliced_8, Spatula_1, ButterKnife_2, Bread_Sliced_1, Knife are in/on CounterTop
  Egg_1 is in/on Cabinet_3
  Cup_1 is inside agent hand
  Cup_0 is in/on Sink
  Cabinet_3 is in/on Floor"""  
  ...
579: 2023/05/02 12:23:27 - 12:23:49: """Goal: Pickup(Cup_0)
  Visual observation: Cabinet_0, Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], SoapBottle, Cup_0 [filled], HousePlant, Sink_Basin, PepperShaker_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Cup_1, Potato_1, Bowl_1 [filled], Knife, Bowl_0 [filled], Fork, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  ButterKnife_0, PaperTowelRoll_1, Spatula_1, Fork, Bread_Sliced_3, Bread_Sliced_1, Spatula_0, Bread_Sliced_7, Bread_Sliced_4, Bread_Sliced_5, Knife, Pot, Bowl_0, Bread_Sliced_2, Potato_1, Cup_1, Pan_0, Bread_Sliced_8, ButterKnife_2, Bread_Sliced_6, Bowl_1, Plate_1, HousePlant, Plate_0 are in/on CounterTop
  PepperShaker_0, SoapBottle, Cup_0, Faucet are in/on Sink"""  
  ...
580: 2023/05/02 12:23:51 - 12:23:54: """Goal: Pour(Sink)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Cup_1, Potato_1, Bowl_1 [filled], Knife, Fork, agent hand, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  Bread_Sliced_3, HousePlant, Bread_Sliced_2, Fork, Potato_1, Bread_Sliced_1, Bowl_0, Spatula_0, Bread_Sliced_7, Pot, Bread_Sliced_5, Knife, Spatula_1, Bread_Sliced_8, Cup_1, Bread_Sliced_6, PaperTowelRoll_1, Plate_1, Bowl_1, Pan_0, Plate_0, ButterKnife_2, ButterKnife_0, DishSponge_0, Bread_Sliced_4 are in/on CounterTop
  Cup_0 is inside agent hand
  Faucet, SoapBottle, Egg_0, PepperShaker_0 are in/on Sink"""  
  ...
581: 2023/05/02 12:23:57 - 12:23:57: """Goal: Place(Sink_Basin)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0, Egg_0, HousePlant, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Cup_1, Potato_1, Bowl_1 [filled], Knife, Fork, agent hand, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  Bread_Sliced_3, HousePlant, Bread_Sliced_2, Fork, Potato_1, Bread_Sliced_1, Bowl_0, Spatula_0, Bread_Sliced_7, Pot, Bread_Sliced_5, Knife, Spatula_1, Bread_Sliced_8, Cup_1, Bread_Sliced_6, PaperTowelRoll_1, Plate_1, Bowl_1, Pan_0, Plate_0, ButterKnife_2, ButterKnife_0, DishSponge_0, Bread_Sliced_4 are in/on CounterTop
  Cup_0 is inside agent hand
  Faucet, SoapBottle, Egg_0, PepperShaker_0 are in/on Sink"""  
  ...
582: 2023/05/02 12:24:00 - 12:24:00: """Goal: ToggleOn(Faucet)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0, Egg_0, HousePlant, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Cup_1, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  Bread_Sliced_3, Pan_0, HousePlant, Bread_Sliced_2, Fork, Potato_1, Bread_Sliced_1, Bowl_0, ButterKnife_0, Bread_Sliced_7, Pot, Bread_Sliced_5, Knife, Spatula_1, Bread_Sliced_8, Cup_1, Bread_Sliced_6, PaperTowelRoll_1, Plate_1, Bowl_1, Spatula_0, ButterKnife_2, Plate_0, DishSponge_0, Bread_Sliced_4 are in/on CounterTop
  Cup_0 is in/on Sink_Basin
  Faucet, SoapBottle, Egg_0, PepperShaker_0 are in/on Sink"""  
  ...
583: 2023/05/02 12:24:04 - 12:24:04: """Goal: ToggleOff(Faucet)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Cup_1, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  Bread_Sliced_3, Pan_0, HousePlant, Bread_Sliced_2, Fork, Potato_1, Bread_Sliced_1, Bowl_0, ButterKnife_0, Bread_Sliced_7, Pot, Bread_Sliced_5, Knife, Spatula_1, Bread_Sliced_8, Cup_1, Bread_Sliced_6, PaperTowelRoll_1, Plate_1, Bowl_1, Spatula_0, ButterKnife_2, Plate_0, DishSponge_0, Bread_Sliced_4 are in/on CounterTop
  Cup_0 is in/on Sink_Basin
  Faucet, SoapBottle, Egg_0, PepperShaker_0 are in/on Sink"""  
  ...
584: 2023/05/02 12:24:07 - 12:24:07: """Goal: Pickup(Cup_0)
  Visual observation: Cabinet_0, Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Pot [filled], Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_1, Cup_1, Potato_1, Bowl_1 [filled], Knife, Fork, Pan_0, Spatula_0, ButterKnife_0, Plate_0
  Bread_Sliced_3, Pan_0, HousePlant, Bread_Sliced_2, Fork, Potato_1, Bread_Sliced_1, Bowl_0, ButterKnife_0, Bread_Sliced_7, Pot, Bread_Sliced_5, Knife, Spatula_1, Bread_Sliced_8, Cup_1, Bread_Sliced_6, PaperTowelRoll_1, Plate_1, Bowl_1, Spatula_0, ButterKnife_2, Plate_0, DishSponge_0, Bread_Sliced_4 are in/on CounterTop
  Cup_0 is in/on Sink_Basin
  Faucet, SoapBottle, Egg_0, PepperShaker_0 are in/on Sink"""  
  ...
585: 2023/05/02 12:24:08 - 12:24:11: """Goal: Pour(Sink)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Cup_0 [filled], Egg_0, HousePlant, Spatula_0, Sink_Basin, PepperShaker_0, DishSponge_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Cup_1, Potato_1, Knife, Fork, agent hand, Pan_0, ButterKnife_0, Plate_0
  Bread_Sliced_6, Fork, DishSponge_0, PaperTowelRoll_1, Cup_1, ButterKnife_0, Bread_Sliced_7, Spatula_0, Spatula_1, Bowl_1, Bread_Sliced_1, Knife, Plate_1, ButterKnife_2, Bread_Sliced_5, Bread_Sliced_4, Pan_0, HousePlant, Bread_Sliced_3, Bread_Sliced_2, Potato_1, Bowl_0, Plate_0, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, PepperShaker_0, Egg_0, Faucet are in/on Sink
  Cup_0 is inside agent hand"""  
  ...
586: 2023/05/02 12:24:13 - 12:24:16: """Goal: Place(CounterTop)
  Visual observation: Plate_1, ButterKnife_2, Spatula_1, Cup_1, Bowl_1 [filled], Egg_1, Cabinet_1 [open], Cabinet_3 [open], Drawer_0, Sink, Bowl_0 [filled], Cup_0, HousePlant, Plate_0, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, PaperTowelRoll_1, Potato_1, Floor, Knife, Fork, agent hand, Pan_0, Spatula_0, ButterKnife_0
  Bread_Sliced_8, Cup_1, Bread_Sliced_7, Fork, Bread_Sliced_5, Potato_1, Spatula_1, Spatula_0, Plate_1, HousePlant, ButterKnife_2, Knife, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Bowl_0, PaperTowelRoll_1, Bread_Sliced_6, Bread_Sliced_4, Pan_0, Plate_0, Bowl_1, ButterKnife_0 are in/on CounterTop
  Egg_1 is in/on Cabinet_3
  Cup_0 is inside agent hand
  Cabinet_3 is in/on Floor"""  
  ...
...
591: 2023/05/02 12:25:42 - 12:25:51: """Goal: Place(Sink_Basin)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Egg_0, HousePlant, Spatula_0, Sink_Basin, PepperShaker_0, DishSponge_0, Spoon, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Cup_1, Potato_1, Knife, Fork, Cup_0, Pan_0, ButterKnife_0, Plate_0, agent hand
  Bread_Sliced_6, Fork, PaperTowelRoll_1, Cup_1, ButterKnife_0, Bread_Sliced_7, Spatula_1, Bowl_1, Bread_Sliced_1, Knife, DishSponge_0, Plate_1, ButterKnife_2, Bread_Sliced_5, Cup_0, HousePlant, Bread_Sliced_4, Pan_0, Spatula_0, Bread_Sliced_3, Bread_Sliced_2, Potato_1, Bowl_0, Plate_0, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, Egg_0, PepperShaker_0, Faucet are in/on Sink
  Spoon is inside agent hand"""  
  ...
592: 2023/05/02 12:25:54 - 12:25:54: """Goal: ToggleOn(Faucet)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Egg_0, HousePlant, Spatula_0, Sink_Basin, PepperShaker_0, DishSponge_0, Spoon, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Cup_1, Potato_1, Knife, Fork, Cup_0, Pan_0, ButterKnife_0, Plate_0
  Spoon is in/on Sink_Basin
  Bread_Sliced_6, Fork, PaperTowelRoll_1, Cup_1, ButterKnife_0, Bread_Sliced_7, Spatula_1, Bowl_1, Bread_Sliced_1, Knife, DishSponge_0, Plate_1, ButterKnife_2, Bread_Sliced_5, Cup_0, HousePlant, Bread_Sliced_4, Pan_0, Spatula_0, Bread_Sliced_3, Bread_Sliced_2, Potato_1, Bowl_0, Plate_0, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, Egg_0, PepperShaker_0, Faucet are in/on Sink"""  
  ...
593: 2023/05/02 12:25:57 - 12:25:57: """Goal: ToggleOff(Faucet)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Egg_0, HousePlant, Spatula_0, Sink_Basin, PepperShaker_0, DishSponge_0, Spoon, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Cup_1, Potato_1, Knife, Fork, Cup_0, Pan_0, ButterKnife_0, Plate_0
  Spoon is in/on Sink_Basin
  Bread_Sliced_6, Fork, PaperTowelRoll_1, Cup_1, ButterKnife_0, Bread_Sliced_7, Spatula_1, Bowl_1, Bread_Sliced_1, Knife, DishSponge_0, Plate_1, ButterKnife_2, Bread_Sliced_5, Cup_0, HousePlant, Bread_Sliced_4, Pan_0, Spatula_0, Bread_Sliced_3, Bread_Sliced_2, Potato_1, Bowl_0, Plate_0, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, Egg_0, PepperShaker_0, Faucet are in/on Sink"""  
  ...
594: 2023/05/02 12:26:00 - 12:26:00: """Goal: Pickup(Spoon)
  Visual observation: Spatula_1, Bowl_1 [filled], Cabinet_1 [open], Faucet [toggled], Drawer_0, Drawer_1, Sink, Bowl_0 [filled], SoapBottle, Egg_0, HousePlant, Spatula_0, Sink_Basin, PepperShaker_0, DishSponge_0, Spoon, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, Plate_1, ButterKnife_2, PaperTowelRoll_1, Cup_1, Potato_1, Knife, Fork, Cup_0, Pan_0, ButterKnife_0, Plate_0
  Spoon is in/on Sink_Basin
  Bread_Sliced_6, Fork, PaperTowelRoll_1, Cup_1, ButterKnife_0, Bread_Sliced_7, Spatula_1, Bowl_1, Bread_Sliced_1, Knife, DishSponge_0, Plate_1, ButterKnife_2, Bread_Sliced_5, Cup_0, HousePlant, Bread_Sliced_4, Pan_0, Spatula_0, Bread_Sliced_3, Bread_Sliced_2, Potato_1, Bowl_0, Plate_0, Bread_Sliced_8 are in/on CounterTop
  SoapBottle, Egg_0, PepperShaker_0, Faucet are in/on Sink"""  
  ...
595: 2023/05/02 12:26:01 - 12:26:06: """Goal: Place(CounterTop)
  Visual observation: Plate_1, ButterKnife_2, Spatula_1, Cup_1, Bowl_1 [filled], Egg_1, Cabinet_1 [open], Cabinet_3 [open], Drawer_0, Bowl_0 [filled], Cup_0, Lettuce_0, HousePlant, Plate_0, Spoon, CounterTop, Bread_Sliced_8, Bread_Sliced_7, Bread_Sliced_6, Bread_Sliced_5, Bread_Sliced_4, Bread_Sliced_3, Bread_Sliced_2, Bread_Sliced_1, PaperTowelRoll_1, Potato_1, Floor, Knife, Fork, Pan_0, Spatula_0, ButterKnife_0, agent hand
  Bread_Sliced_3, Bowl_0, Bread_Sliced_2, Cup_0, Bread_Sliced_1, Pan_0, Bread_Sliced_7, Bread_Sliced_5, ButterKnife_0, Plate_0, Cup_1, Bowl_1, Knife, Bread_Sliced_8, Fork, Bread_Sliced_6, Plate_1, ButterKnife_2, PaperTowelRoll_1, Spatula_0, Spatula_1, HousePlant, Potato_1, Bread_Sliced_4 are in/on CounterTop
  Egg_1, Lettuce_0 are in/on Cabinet_3
  Cabinet_3 is in/on Floor
  Spoon is inside agent hand"""  
  ...
...
597: 2023/05/03 09:16:57 - 09:18:15: """Goal: Open(Fridge)
  Visual observation: CounterTop_1, Drawer_3, Cabinet_12, Pencil, Fridge
  Speech:
  2023-05-03 09:17:38.980027: 1 slice of lettuce
  2023-05-03 09:17:55.524558: it is on the cabinet right to the basin"""  
  ...
...
603: 2023/05/03 09:18:43 - 09:18:59: """Goal: Open(Cabinet_18)
  Visual observation: Fork_2, ButterKnife_1, Drawer_2, Cabinet_9, Cabinet_10, Cabinet_18, Drawer_8, Faucet [toggled], Cabinet_20, Cabinet_21, Cabinet_22, Sink, Apple, Fork_0, Window, PaperTowelRoll, Sink_Basin, SoapBottle, DishSponge, Floor, CounterTop_2, Knife
  ButterKnife_1, PaperTowelRoll, Fork_2, Fork_0 are in/on Sink_Basin
  SoapBottle, Faucet, Knife, Apple, DishSponge are in/on CounterTop_2
  Cabinet_10, Cabinet_20, Cabinet_18, Cabinet_21, Cabinet_9 are in/on Floor
  Speech:
  2023-05-03 09:18:53.902892: 1 slice of tomato which is inside the cabinet below the basin"""  
  ...
604: 2023/05/03 09:19:03 - 09:19:03: """Goal: Open(Cabinet_21)
  Visual observation: Fork_2, ButterKnife_1, Drawer_2, Cabinet_9, Cabinet_10, Cabinet_18 [open], Drawer_8, Faucet [toggled], Cabinet_20, Cabinet_21, Cabinet_22, Sink, Apple, Potato_0, Fork_0, Window, PaperTowelRoll, Sink_Basin, SoapBottle, DishSponge, Floor, CounterTop_2, Knife
  Cabinet_9, Cabinet_21, Cabinet_10, Cabinet_20, Cabinet_18 are in/on Floor
  DishSponge, Faucet, SoapBottle, Knife, Apple are in/on CounterTop_2
  PaperTowelRoll, ButterKnife_1, Fork_0, Fork_2 are in/on Sink_Basin"""  
  ...
605: 2023/05/03 09:19:07 - 09:19:07: """Goal: Pickup(Tomato_1)
  Visual observation: Tomato_1, Fork_2, ButterKnife_1, Drawer_2, Cabinet_9, Cabinet_10, Cabinet_18 [open], Drawer_8, Faucet [toggled], Cabinet_21 [open], Cabinet_22, Sink, Apple, Potato_0, Fork_0, Window, PaperTowelRoll, Sink_Basin, SoapBottle, DishSponge, Floor, CounterTop_2, Knife
  DishSponge, SoapBottle, Knife, Faucet, Apple are in/on CounterTop_2
  Cabinet_21, Cabinet_9, Cabinet_10, Cabinet_18 are in/on Floor
  PaperTowelRoll, Fork_2, Fork_0, ButterKnife_1 are in/on Sink_Basin"""  
  ...
606: 2023/05/03 09:19:09 - 09:19:14: """Goal: Place(CounterTop_2)
  Visual observation: Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Tomato_1, Cabinet_6, Drawer_4, Cabinet_10, Drawer_6, Cabinet_17, Drawer_8, Cabinet_22, Cabinet_24, Knife, Spatula, agent hand, Floor, CounterTop_2
  Cabinet_10 is in/on Floor
  Lettuce_Sliced_5, Lettuce_Sliced_1, Lettuce_Sliced_4, Knife, Lettuce_Sliced_0, Lettuce_Sliced_3, Lettuce_Sliced_2, Spatula are in/on CounterTop_2
  Tomato_1 is inside agent hand"""  
  ...
...
610: 2023/05/03 09:19:27 - 09:19:32: """Goal: Pickup(Potato_0)
  Visual observation: Fork_2, ButterKnife_1, Drawer_2, Cabinet_9, Cabinet_10, Cabinet_18 [open], Drawer_8, Faucet [toggled], Cabinet_21 [open], Cabinet_22, Sink, Apple, Potato_0, Fork_0, Window, PaperTowelRoll, Sink_Basin, SoapBottle, DishSponge, CounterTop_2, Tomato_1_Sliced_6, Tomato_1_Sliced_5, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, Floor, Knife
  Tomato_1_Sliced_2, DishSponge, Tomato_1_Sliced_1, Tomato_1_Sliced_6, Tomato_1_Sliced_0, Tomato_1_Sliced_5, Apple, Tomato_1_Sliced_4, Tomato_1_Sliced_3, SoapBottle, Faucet, Knife are in/on CounterTop_2
  Cabinet_10, Cabinet_18, Cabinet_9, Cabinet_21 are in/on Floor
  Fork_0, PaperTowelRoll, Fork_2, ButterKnife_1 are in/on Sink_Basin"""  
  ...
611: 2023/05/03 09:19:34 - 09:19:39: """Goal: Place(CounterTop_2)
  Visual observation: Tomato_1_Sliced_6, Tomato_1_Sliced_5, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Cabinet_6, Drawer_4, Cabinet_10, Drawer_6, Cabinet_17, Drawer_8, Cabinet_22, Cabinet_24, Knife, Potato_0, Spatula, CounterTop_2, Floor, agent hand
  Lettuce_Sliced_3, Spatula, Lettuce_Sliced_2, Lettuce_Sliced_5, Tomato_1_Sliced_2, Tomato_1_Sliced_5, Lettuce_Sliced_4, Tomato_1_Sliced_1, Lettuce_Sliced_0, Tomato_1_Sliced_4, Tomato_1_Sliced_0, Lettuce_Sliced_1, Knife, Tomato_1_Sliced_3, Tomato_1_Sliced_6 are in/on CounterTop_2
  Cabinet_10 is in/on Floor
  Potato_0 is inside agent hand"""  
  ...
...
663: 2023/05/04 10:40:08 - 10:41:03: """Goal: Pickup(SaltShaker)
  Visual observation: Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Plate, Toaster, Kettle_0 [filled], Fridge, WineBottle_0, Cup, Pan, Sink_Basin, SaltShaker, PepperShaker, ButterKnife, Spoon_0, Faucet
  Speech:
  2023-05-04 10:40:08.047377: hello
  2023-05-04 10:40:36.125694: Can you please make a lettuce sandwich with toasted bread."""  
  ...
664: 2023/05/04 10:41:07 - 10:41:07: """Goal: Place(CounterTop_0)
  Visual observation: Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Plate, Toaster, Kettle_0 [filled], Fridge, WineBottle_0, Cup, Pan, Sink_Basin, SaltShaker, PepperShaker, ButterKnife, Spoon_0, Faucet, agent hand
  SaltShaker is inside agent hand
  PepperShaker, ButterKnife, Cup are in/on Sink_Basin"""  
  ...
665: 2023/05/04 10:41:10 - 10:41:10: """Goal: Pickup(ButterKnife)
  Visual observation: Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Plate, Toaster, Kettle_0 [filled], Fridge, WineBottle_0, Cup, Pan, Sink_Basin, PepperShaker, ButterKnife, Spoon_0, Faucet, SaltShaker
  PepperShaker, Cup, ButterKnife are in/on Sink_Basin
  Kettle_0, SaltShaker, Pan, Spoon_0, Plate, WineBottle_0, Bowl_2, Toaster are in/on CounterTop_0"""  
  ...
666: 2023/05/04 10:41:13 - 10:41:18: """Goal: Slice(Bread_0)
  Visual observation: Bowl_2, Pot_1 [dirty, filled], CounterTop_0, Drawer_1, StoveBurner_0, StoveBurner_1, Cabinet_1, StoveBurner_2, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_4, Cabinet_8, StoveBurner_3, StoveKnob_2, StoveKnob_3, Bread_0, Tomato_0, CoffeeMachine [toggled], Pan, ButterKnife, Microwave [toggled], SaltShaker, agent hand
  Tomato_0, CoffeeMachine, SaltShaker, Pan, Bread_0, Bowl_2 are in/on CounterTop_0
  ButterKnife is inside agent hand"""  
  ...
...
669: 2023/05/04 10:41:26 - 10:41:42: """Goal: Place(Toaster)
  Visual observation: Bread_0_Sliced_3, Bowl_2, CounterTop_0, Sink, Plate, Toaster, Kettle_0 [filled], Fridge, WineBottle_0, Cup, Pan, Sink_Basin, PepperShaker, Spoon_0, Faucet, agent hand, SaltShaker, ButterKnife
  Spoon_0, ButterKnife, Plate, WineBottle_0, Toaster, Kettle_0, SaltShaker, Bowl_2, Pan are in/on CounterTop_0
  PepperShaker, Cup are in/on Sink_Basin
  Bread_0_Sliced_3 is inside agent hand"""  
  ...
670: 2023/05/04 10:41:46 - 10:41:46: """Goal: ToggleOn(Toaster)
  Visual observation: Bread_0_Sliced_3, Bowl_2, CounterTop_0, Sink, Plate, Toaster, Kettle_0 [filled], Fridge, WineBottle_0, Cup, Pan, Sink_Basin, PepperShaker, Spoon_0, Faucet, SaltShaker, ButterKnife
  Spoon_0, Plate, WineBottle_0, Toaster, Kettle_0, SaltShaker, ButterKnife, Bowl_2, Bread_0_Sliced_3, Pan are in/on CounterTop_0
  PepperShaker, Cup are in/on Sink_Basin
  Bread_0_Sliced_3 is in/on Toaster"""  
  ...
671: 2023/05/04 10:41:49 - 10:42:41: """Goal: Open(Fridge)
  Visual observation: WineBottle_1 [filled], CounterTop_0, Sink, Cabinet_0, Cabinet_7, Fridge, PepperShaker, GarbageCan, Toaster [toggled], Bread_0_Sliced_3 [cooked], Sink_Basin, SaltShaker, ButterKnife
  Bread_0_Sliced_3 is in/on Toaster
  SaltShaker, Toaster, ButterKnife, Bread_0_Sliced_3 are in/on CounterTop_0
  PepperShaker is in/on Sink_Basin
  Speech:
  2023-05-04 10:42:28.533093: Place the 2 pieces of toasted bread and one piece of lettuce on a plate"""  
  ...
...
673: 2023/05/04 10:42:56 - 10:43:02: """Goal: Pickup(Bread_0_Sliced_2)
  Visual observation: Bread_0_Sliced_5, Bread_0_Sliced_4, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2, Bread_0_Sliced_1, Bread_0__0, Bowl_2, CounterTop_0, Drawer_1, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_4, Cabinet_7, Cabinet_8, Toaster [toggled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, PepperShaker, ButterKnife, Faucet
  Bread_0_Sliced_2, ButterKnife, Toaster, Bread_0_Sliced_1, Bread_0_Sliced_4, Bread_0__0, CoffeeMachine, SaltShaker, Bread_0_Sliced_3, Bowl_2, WineBottle_0, Pan, Tomato_0, Bread_0_Sliced_5 are in/on CounterTop_0
  PepperShaker, Cup are in/on Sink_Basin
  Bread_0_Sliced_3 is in/on Toaster
  Speech:
  2023-05-04 10:42:57.077944: lettuce is in lower cabinet to left of stove"""  
  ...
674: 2023/05/04 10:43:04 - 10:43:13: """Goal: Place(CounterTop_0)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2, Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet, agent hand
  Bread_0_Sliced_3, Kettle_0, CoffeeMachine, SaltShaker, Plate, Tomato_0, Toaster, ButterKnife, WineBottle_0, Bowl_2, Pan are in/on CounterTop_0
  Bread_0_Sliced_2 is inside agent hand
  Bread_0_Sliced_3 is in/on Toaster
  Cup is in/on Sink_Basin"""  
  ...
675: 2023/05/04 10:43:16 - 10:43:16: """Goal: Pickup(Bread_0_Sliced_3)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2, Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet
  Bread_0_Sliced_3, Kettle_0, CoffeeMachine, Bread_0_Sliced_2, SaltShaker, Plate, Tomato_0, Toaster, ButterKnife, WineBottle_0, Bowl_2, Pan are in/on CounterTop_0
  Bread_0_Sliced_3 is in/on Toaster
  Cup is in/on Sink_Basin"""  
  ...
676: 2023/05/04 10:43:20 - 10:43:20: """Goal: Place(CounterTop_0)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2, Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet, agent hand
  Kettle_0, CoffeeMachine, Bread_0_Sliced_2, SaltShaker, Plate, Tomato_0, Toaster, ButterKnife, WineBottle_0, Bowl_2, Pan are in/on CounterTop_0
  Bread_0_Sliced_3 is inside agent hand
  Cup is in/on Sink_Basin"""  
  ...
677: 2023/05/04 10:43:23 - 10:43:23: """Goal: Pickup(Bread_0_Sliced_2)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2, Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet
  Bread_0_Sliced_3, Kettle_0, CoffeeMachine, Bread_0_Sliced_2, SaltShaker, Plate, Tomato_0, Toaster, ButterKnife, WineBottle_0, Bowl_2, Pan are in/on CounterTop_0
  Cup is in/on Sink_Basin"""  
  ...
678: 2023/05/04 10:43:26 - 10:43:26: """Goal: Place(Toaster)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2, Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet, agent hand
  Bread_0_Sliced_3, Kettle_0, CoffeeMachine, SaltShaker, Plate, Tomato_0, Toaster, ButterKnife, WineBottle_0, Bowl_2, Pan are in/on CounterTop_0
  Bread_0_Sliced_2 is inside agent hand
  Cup is in/on Sink_Basin"""  
  ...
679: 2023/05/04 10:43:33 - 10:43:33: """Goal: Pickup(Kettle_0)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet
  Bread_0_Sliced_3, Kettle_0, CoffeeMachine, SaltShaker, Bread_0_Sliced_2, Plate, Tomato_0, Toaster, ButterKnife, WineBottle_0, Bowl_2, Pan are in/on CounterTop_0
  Bread_0_Sliced_2 is in/on Toaster
  Cup is in/on Sink_Basin"""  
  ...
680: 2023/05/04 10:43:37 - 10:43:37: """Goal: Place(CounterTop_0)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet, agent hand
  Bread_0_Sliced_3, CoffeeMachine, SaltShaker, Bread_0_Sliced_2, Plate, Tomato_0, Toaster, ButterKnife, WineBottle_0, Bowl_2, Pan are in/on CounterTop_0
  Bread_0_Sliced_2 is in/on Toaster
  Kettle_0 is inside agent hand
  Cup is in/on Sink_Basin"""  
  ...
681: 2023/05/04 10:43:40 - 10:43:49: """Goal: Pickup(Plate)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Plate, Toaster [toggled], Kettle_0 [filled], Fridge [open], WineBottle_0, Cup, Pan, Sink_Basin, PepperShaker, Spoon_0, Faucet, SaltShaker, ButterKnife
  SaltShaker, Bread_0_Sliced_3, WineBottle_0, ButterKnife, Kettle_0, Bread_0_Sliced_2, Plate, Spoon_0, Toaster, Pan, Bowl_2 are in/on CounterTop_0
  Cup, PepperShaker are in/on Sink_Basin
  Bread_0_Sliced_2 is in/on Toaster"""  
  ...
682: 2023/05/04 10:43:53 - 10:44:03: """Goal: Place(CounterTop_0)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, Sink_Basin, PepperShaker, ButterKnife, Spoon_0, Faucet, agent hand, SaltShaker
  Bread_0_Sliced_3, Kettle_0, SaltShaker, Spoon_0, Bread_0_Sliced_2, Tomato_0, Toaster, WineBottle_0, Bowl_2, ButterKnife are in/on CounterTop_0
  Cup, PepperShaker are in/on Sink_Basin
  Bread_0_Sliced_2 is in/on Toaster
  Plate is inside agent hand"""  
  ...
683: 2023/05/04 10:44:06 - 10:44:06: """Goal: Pickup(Bread_0_Sliced_3)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, Pan, Sink_Basin, SaltShaker, PepperShaker, ButterKnife, Spoon_0, Faucet
  Bread_0_Sliced_3, Kettle_0, Pan, Bread_0_Sliced_2, Tomato_0, Toaster, ButterKnife, WineBottle_0, Plate, Bowl_2, Spoon_0, SaltShaker are in/on CounterTop_0
  Bread_0_Sliced_2 is in/on Toaster
  PepperShaker, Cup are in/on Sink_Basin"""  
  ...
684: 2023/05/04 10:44:10 - 10:44:10: """Goal: Place(Plate)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, Pan, Sink_Basin, PepperShaker, ButterKnife, Spoon_0, Faucet, agent hand, SaltShaker
  Kettle_0, Pan, ButterKnife, Bread_0_Sliced_2, Tomato_0, Toaster, SaltShaker, Spoon_0, WineBottle_0, Plate, Bowl_2 are in/on CounterTop_0
  Bread_0_Sliced_2 is in/on Toaster
  Cup, PepperShaker are in/on Sink_Basin
  Bread_0_Sliced_3 is inside agent hand"""  
  ...
685: 2023/05/04 10:44:14 - 10:44:14: """Goal: Pickup(Bread_0_Sliced_2)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, Pan, Sink_Basin, SaltShaker, PepperShaker, ButterKnife, Spoon_0, Faucet
  Bread_0_Sliced_3, Kettle_0, Pan, Bread_0_Sliced_2, Tomato_0, Toaster, ButterKnife, WineBottle_0, Plate, Bowl_2, Spoon_0, SaltShaker are in/on CounterTop_0
  Bread_0_Sliced_3 is in/on Plate
  Bread_0_Sliced_2 is in/on Toaster
  PepperShaker, Cup are in/on Sink_Basin"""  
  ...
686: 2023/05/04 10:44:17 - 10:44:17: """Goal: Place(Plate)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, Pan, Sink_Basin, PepperShaker, ButterKnife, Spoon_0, Faucet, agent hand, SaltShaker
  Bread_0_Sliced_3, Kettle_0, Pan, ButterKnife, Tomato_0, Toaster, Spoon_0, WineBottle_0, Plate, Bowl_2, SaltShaker are in/on CounterTop_0
  Bread_0_Sliced_3 is in/on Plate
  Cup, PepperShaker are in/on Sink_Basin
  Bread_0_Sliced_2 is inside agent hand"""  
  ...
687: 2023/05/04 10:44:23 - 10:44:34: """Goal: Open(Cabinet_10)
  Visual observation: Bread_0_Sliced_5, Bread_0_Sliced_4, Bread_0_Sliced_1, Bread_0__0, Pot_1 [dirty, filled], SoapBottle_1, CounterTop_0, Drawer_0, Drawer_1, StoveBurner_0, StoveBurner_1, Cabinet_1, StoveBurner_2, CounterTop_1, Drawer_2, Cabinet_3, Cabinet_4, Cabinet_9, Cabinet_10, StoveBurner_3, Knife, StoveKnob_2, StoveKnob_3, Fork_0, CoffeeMachine [toggled], ButterKnife, Microwave [toggled], Plate, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Kettle_0 [filled], SaltShaker
  Bread_0_Sliced_3, ButterKnife, Bread_0__0, Kettle_0, Bread_0_Sliced_5, Plate, CoffeeMachine, Bread_0_Sliced_2, SaltShaker, Bread_0_Sliced_4, Bread_0_Sliced_1 are in/on CounterTop_0
  Bread_0_Sliced_2, Bread_0_Sliced_3 are in/on Plate
  SoapBottle_1, Fork_0, Knife are in/on CounterTop_1"""  
  ...
...
689: 2023/05/04 10:44:40 - 10:44:49: """Goal: Place(CounterTop_0)
  Visual observation: Bread_0_Sliced_3 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Plate, Toaster [toggled], Kettle_0 [filled], Fridge [open], WineBottle_0, Cup, Lettuce, Pan, Sink_Basin, PepperShaker, Spoon_0, Faucet, Bread_0_Sliced_2 [cooked], Floor, agent hand, SaltShaker, ButterKnife
  WineBottle_0, SaltShaker, Plate, Bread_0_Sliced_2, Kettle_0, Spoon_0, ButterKnife, Pan, Bowl_2, Bread_0_Sliced_3, Toaster are in/on CounterTop_0
  Lettuce is inside agent hand
  Fridge is in/on Floor
  Cup, PepperShaker are in/on Sink_Basin
  Bread_0_Sliced_3, Bread_0_Sliced_2 are in/on Plate"""  
  ...
690: 2023/05/04 10:44:52 - 10:44:57: """Goal: Pickup(ButterKnife)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Lettuce, Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet
  Bread_0_Sliced_3, Kettle_0, CoffeeMachine, Bread_0_Sliced_2, Tomato_0, Toaster, SaltShaker, WineBottle_0, Plate, Bowl_2, Lettuce, ButterKnife, Pan are in/on CounterTop_0
  Bread_0_Sliced_2, Bread_0_Sliced_3 are in/on Plate
  Cup is in/on Sink_Basin"""  
  ...
691: 2023/05/04 10:45:00 - 10:45:00: """Goal: Slice(Lettuce)
  Visual observation: Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Lettuce, Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet, agent hand
  Bread_0_Sliced_3, Kettle_0, CoffeeMachine, Bread_0_Sliced_2, Tomato_0, Toaster, SaltShaker, WineBottle_0, Plate, Bowl_2, Lettuce, Pan are in/on CounterTop_0
  Bread_0_Sliced_2, Bread_0_Sliced_3 are in/on Plate
  Cup is in/on Sink_Basin
  ButterKnife is inside agent hand"""  
  ...
692: 2023/05/04 10:45:03 - 10:45:03: """Goal: Place(CounterTop_0)
  Visual observation: Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet, Lettuce, agent hand
  Lettuce_Sliced_6, SaltShaker, Lettuce_Sliced_1, Plate, Lettuce, CoffeeMachine, Lettuce_Sliced_4, Pan, Lettuce_Sliced_5, Kettle_0, Bread_0_Sliced_2, WineBottle_0, Bowl_2, Tomato_0, Lettuce_Sliced_0, Bread_0_Sliced_3, Toaster, Lettuce_Sliced_2, Lettuce_Sliced_3 are in/on CounterTop_0
  Bread_0_Sliced_3, Lettuce_Sliced_0, Bread_0_Sliced_2 are in/on Plate
  Cup is in/on Sink_Basin
  ButterKnife is inside agent hand"""  
  ...
693: 2023/05/04 10:45:07 - 10:45:07: """Goal: Pickup(Lettuce_Sliced_4)
  Visual observation: Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet
  ButterKnife, Lettuce_Sliced_6, SaltShaker, Lettuce_Sliced_1, Plate, CoffeeMachine, Lettuce_Sliced_4, Pan, Lettuce_Sliced_5, Kettle_0, Bread_0_Sliced_2, WineBottle_0, Bowl_2, Tomato_0, Lettuce_Sliced_0, Bread_0_Sliced_3, Toaster, Lettuce_Sliced_2, Lettuce_Sliced_3 are in/on CounterTop_0
  Bread_0_Sliced_3, Bread_0_Sliced_2 are in/on Plate
  Cup is in/on Sink_Basin"""  
  ...
694: 2023/05/04 10:45:12 - 10:45:15: """Goal: Place(Plate)
  Visual observation: Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet, agent hand
  ButterKnife, Lettuce_Sliced_6, SaltShaker, Lettuce_Sliced_1, Plate, CoffeeMachine, Pan, Lettuce_Sliced_5, Kettle_0, Bread_0_Sliced_2, Bowl_2, WineBottle_0, Tomato_0, Lettuce_Sliced_0, Bread_0_Sliced_3, Toaster, Lettuce_Sliced_2, Lettuce_Sliced_3 are in/on CounterTop_0
  Bread_0_Sliced_3, Bread_0_Sliced_2 are in/on Plate
  Lettuce_Sliced_4 is inside agent hand
  Cup is in/on Sink_Basin"""  
  ...
695: 2023/05/04 10:45:22 - 10:45:22: """Goal: Noop
  Visual observation: Lettuce_Sliced_6, Lettuce_Sliced_5, Lettuce_Sliced_4, Lettuce_Sliced_3, Lettuce_Sliced_2, Lettuce_Sliced_1, Lettuce_Sliced_0, Bread_0_Sliced_3 [cooked], Bread_0_Sliced_2 [cooked], Bowl_2, CounterTop_0, Sink, Cabinet_0, Drawer_2, Cabinet_2, Cabinet_3, Cabinet_7, Cabinet_8, Plate, Toaster [toggled], Kettle_0 [filled], WineBottle_0, Tomato_0, Cup, CoffeeMachine [toggled], Pan, Sink_Basin, SaltShaker, ButterKnife, Faucet
  ButterKnife, Lettuce_Sliced_6, SaltShaker, Lettuce_Sliced_1, Plate, CoffeeMachine, Lettuce_Sliced_4, Pan, Lettuce_Sliced_5, Kettle_0, Bread_0_Sliced_2, WineBottle_0, Bowl_2, Tomato_0, Lettuce_Sliced_0, Bread_0_Sliced_3, Toaster, Lettuce_Sliced_2, Lettuce_Sliced_3 are in/on CounterTop_0
  Bread_0_Sliced_3, Lettuce_Sliced_4, Bread_0_Sliced_2 are in/on Plate
  Cup is in/on Sink_Basin
  Speech:
  2023-05-04 10:45:22.937402: great job task done"""  
  ...
696: 2023/05/05 10:59:17 - 11:00:11: """Goal: Open(Fridge)
  Visual observation: GarbageCan, Fridge
  Speech:
  2023-05-05 10:59:39.379496: Hi. First we need to get the coffee mug from the fridge and make coffee."""  
  ...
...
699: 2023/05/05 11:00:22 - 11:00:34: """Goal: Place(CoffeeMachine)
  Visual observation: Window_0, Drawer_0, Cabinet_5, Cabinet_6, CoffeeMachine [toggled], Knife, PepperShaker_0, CellPhone_0, Mug, Faucet, CounterTop_0, Sink_Basin, agent hand
  CellPhone_0, Window_0, CoffeeMachine, PepperShaker_0 are in/on CounterTop_0
  Mug is inside agent hand
  Knife is in/on Sink_Basin"""  
  ...
700: 2023/05/05 11:00:40 - 11:00:40: """Goal: ToggleOff(CoffeeMachine)
  Visual observation: Window_0, Drawer_0, Cabinet_5, Cabinet_6, CoffeeMachine [toggled], Knife, PepperShaker_0, CellPhone_0, Mug [filled], Faucet, CounterTop_0
  CellPhone_0, Window_0, CoffeeMachine, Mug, PepperShaker_0 are in/on CounterTop_0
  Mug is in/on CoffeeMachine"""  
  ...
701: 2023/05/05 11:00:40 - 11:00:55: """Goal: Open(Cabinet_7)
  Visual observation: Egg_2, Window_0, Cabinet_7, Bowl_0 [dirty, filled], Faucet, CounterTop_0, CoffeeMachine, Mug [filled]
  Egg_2, Bowl_0, Window_0 are in/on CounterTop_0
  Mug is in/on CoffeeMachine
  Speech:
  2023-05-05 11:00:40.966688: Next we need the bread in the upper cabinet to the right of the sink sliced"""  
  ...
702: 2023/05/05 11:00:58 - 11:00:58: """Goal: Pickup(Bread_1)
  Visual observation: Bread_1, Egg_2, Window_0, Cabinet_7 [open], Bowl_0 [dirty, filled], Faucet, CounterTop_0, CoffeeMachine, Mug [filled]
  Egg_2, Bowl_0, Window_0 are in/on CounterTop_0
  Mug is in/on CoffeeMachine"""  
  ...
703: 2023/05/05 11:01:00 - 11:01:02: """Goal: Close(Cabinet_7)
  Visual observation: Bread_1, Window_0, Cabinet_7 [open], Bowl_0 [dirty, filled], Faucet, agent hand, CounterTop_0, CoffeeMachine, Mug [filled]
  Bowl_0, Window_0 are in/on CounterTop_0
  Mug is in/on CoffeeMachine
  Bread_1 is inside agent hand
  Speech:
  2023-05-05 11:01:00.505622: The knife is in the sink"""  
  ...
704: 2023/05/05 11:01:06 - 11:01:11: """Goal: Place(CounterTop_0)
  Visual observation: Bread_1, Egg_2, Ladle_1, Window_0, Cabinet_7 [open], Cabinet_8, Knife, Bowl_0 [dirty, filled], Faucet, agent hand, CounterTop_0, CoffeeMachine, Mug [filled]
  Bowl_0, Egg_2, Ladle_1, Window_0 are in/on CounterTop_0
  Bread_1 is inside agent hand
  Mug is in/on CoffeeMachine"""  
  ...
705: 2023/05/05 11:01:15 - 11:01:15: """Goal: Pickup(Knife)
  Visual observation: Bread_1, Egg_2, Ladle_1, Window_0, Cabinet_7 [open], Cabinet_8, Knife, Bowl_0 [dirty, filled], Faucet, CounterTop_0, CoffeeMachine, Mug [filled]
  Egg_2, Ladle_1, Bread_1, Window_0, Bowl_0 are in/on CounterTop_0
  Mug is in/on CoffeeMachine"""  
  ...
706: 2023/05/05 11:01:18 - 11:01:18: """Goal: Slice(Bread_1)
  Visual observation: Bread_1, Egg_2, Ladle_1, Window_0, Cabinet_7 [open], Cabinet_8, Knife, Bowl_0 [dirty, filled], Faucet, CounterTop_0, agent hand, CoffeeMachine, Mug [filled]
  Egg_2, Ladle_1, Bread_1, Window_0, Bowl_0 are in/on CounterTop_0
  Knife is inside agent hand
  Mug is in/on CoffeeMachine"""  
  ...
707: 2023/05/05 11:01:22 - 11:01:22: """Goal: Place(CounterTop_0)
  Visual observation: Bread_1_Sliced_7, Bread_1_Sliced_6, Bread_1_Sliced_5, Bread_1_Sliced_4, Bread_1_Sliced_3, Bread_1_Sliced_2, Bread_1_Sliced_1, Bread_1__0, Egg_2, Ladle_1, Window_0, Cabinet_7 [open], Cabinet_8, Knife, Bowl_0 [dirty, filled], Faucet, CounterTop_0, Bread_1_Sliced_8, agent hand, CoffeeMachine, Mug [filled]
  Bread_1_Sliced_8, Window_0, Bread_1__0, Bread_1_Sliced_3, Bread_1_Sliced_6, Egg_2, Bread_1_Sliced_2, Bread_1_Sliced_5, Bowl_0, Bread_1_Sliced_7, Ladle_1, Bread_1_Sliced_1, Bread_1_Sliced_4 are in/on CounterTop_0
  Mug is in/on CoffeeMachine
  Knife is inside agent hand"""  
  ...
708: 2023/05/05 11:01:26 - 11:01:26: """Goal: Pickup(Bread_1_Sliced_6)
  Visual observation: Bread_1_Sliced_7, Bread_1_Sliced_6, Bread_1_Sliced_5, Bread_1_Sliced_4, Bread_1_Sliced_3, Bread_1_Sliced_2, Bread_1_Sliced_1, Bread_1__0, Egg_2, Ladle_1, Window_0, Cabinet_7 [open], Cabinet_8, Knife, Bowl_0 [dirty, filled], Faucet, CounterTop_0, Bread_1_Sliced_8, CoffeeMachine, Mug [filled]
  Bread_1_Sliced_8, Window_0, Bread_1__0, Bread_1_Sliced_3, Bread_1_Sliced_6, Egg_2, Knife, Bread_1_Sliced_2, Bread_1_Sliced_5, Bowl_0, Bread_1_Sliced_7, Ladle_1, Bread_1_Sliced_1, Bread_1_Sliced_4 are in/on CounterTop_0
  Mug is in/on CoffeeMachine"""  
  ...
709: 2023/05/05 11:01:29 - 11:01:42: """Goal: Place(Toaster)
  Visual observation: Bread_1_Sliced_6, StoveBurner_0, Drawer_1, Drawer_2, Drawer_3, StoveBurner_1, Cabinet_2, Drawer_5, Cabinet_5, Drawer_6, StoveBurner_2, Drawer_7, Drawer_9, StoveBurner_4, Drawer_10, Window_1, StoveBurner_5, Microwave, Egg_0, SaltShaker, PepperShaker_0, Toaster, CounterTop_0, Bread_1_Sliced_8, Bread_1_Sliced_7, agent hand, Bread_1_Sliced_5, Bread_1_Sliced_4, Bread_1_Sliced_3, Bread_1_Sliced_2, Bread_1_Sliced_1, Knife, CoffeeMachine, Mug [filled]
  Bread_1_Sliced_2, SaltShaker, PepperShaker_0, Bread_1_Sliced_8, Bread_1_Sliced_4, Bread_1_Sliced_5, Microwave, Bread_1_Sliced_1, Egg_0, Knife, Window_1, Bread_1_Sliced_7, Toaster, Bread_1_Sliced_3 are in/on CounterTop_0
  Mug is in/on CoffeeMachine
  Bread_1_Sliced_6 is inside agent hand
  Speech:
  2023-05-05 11:01:29.405825: We need to toast 1 slice"""  
  ...
...
714: 2023/05/05 11:02:07 - 11:02:39: """Goal: Pickup(Knife)
  Visual observation: Bread_1_Sliced_5, Bread_1_Sliced_4, Bread_1_Sliced_3, Bread_1_Sliced_2, Bread_1__0, Egg_2, Cabinet_7 [open], Cabinet_8, Knife, Bowl_0 [dirty, filled], CounterTop_0, Bread_1_Sliced_8, Bread_1_Sliced_7, Bread_1_Sliced_6 [cooked], Bread_1_Sliced_1, CoffeeMachine, Mug [filled]
  Mug is in/on CoffeeMachine
  Bread_1_Sliced_4, Bread_1_Sliced_5, Bread_1_Sliced_6, Egg_2, Bread_1_Sliced_1, Bread_1_Sliced_8, Bowl_0, Bread_1__0, Knife, Bread_1_Sliced_7, Bread_1_Sliced_3, Bread_1_Sliced_2 are in/on CounterTop_0
  Speech:
  2023-05-05 11:02:20.854866: Great ). Next we need to slice the lettuce on the nook behind you."""  
  ...
715: 2023/05/05 11:02:40 - 11:02:52: """Goal: Slice(Lettuce_1)
  Visual observation: Lettuce_1, Cabinet_4, Spatula, Knife, Tomato_0, Potato_0, Chair, CounterTop_0, Bread_1_Sliced_8, Bread_1_Sliced_7, Bread_1_Sliced_6 [cooked], Bread_1_Sliced_5, Bread_1_Sliced_4, Bread_1_Sliced_3, Bread_1_Sliced_2, Bread_1_Sliced_1, agent hand, CoffeeMachine, Mug [filled]
  Bread_1_Sliced_3, Bread_1_Sliced_8, Bread_1_Sliced_4, Bread_1_Sliced_2, Bread_1_Sliced_5, Bread_1_Sliced_1, Bread_1_Sliced_6, Bread_1_Sliced_7 are in/on CounterTop_0
  Knife is inside agent hand
  Mug is in/on CoffeeMachine"""  
  ...
...
727: 2023/05/05 11:05:22 - 11:06:11: """Goal: Pickup(Bread_1_Sliced_7)
  Visual observation: Bread_1_Sliced_7, Bread_1_Sliced_5, Bread_1_Sliced_4, Bread_1_Sliced_3, Bread_1_Sliced_2, Bread_1_Sliced_1, Bread_1__0, Egg_2, Ladle_1, Window_0, Drawer_0, Cabinet_7 [open], Cabinet_8, Bowl_0 [dirty, filled], Faucet, CounterTop_1, Lettuce_1_Sliced_5, Bread_1_Sliced_6 [cooked], CounterTop_0, Plate, Knife, CoffeeMachine, Mug [filled]
  Window_0, Bowl_0, Bread_1_Sliced_1, Egg_2, Ladle_1, Bread_1_Sliced_4, Bread_1__0, Bread_1_Sliced_3, Bread_1_Sliced_2, Bread_1_Sliced_5, Bread_1_Sliced_7 are in/on CounterTop_0
  Lettuce_1_Sliced_5, Plate, Knife, Bread_1_Sliced_6 are in/on CounterTop_1
  Mug is in/on CoffeeMachine
  Speech:
  2023-05-05 11:05:39.321581: it needs 1 more slice of toast on the plate.
  2023-05-05 11:05:52.868834: That's my bad. Sorry"""  
  ...
728: 2023/05/05 11:06:14 - 11:06:25: """Goal: Place(Toaster)
  Visual observation: Bread_1_Sliced_7, Pan_2, StoveBurner_0, Drawer_1, Drawer_2, Drawer_3, StoveBurner_1, Cabinet_2, Drawer_5, Drawer_6, StoveBurner_2, Drawer_7, StoveBurner_3, Drawer_9, StoveBurner_4, Drawer_10, Window_1, StoveBurner_5, StoveKnob_0 [toggled], StoveKnob_4, StoveKnob_5 [toggled], Microwave, Egg_0, SaltShaker, Toaster [toggled], CounterTop_1, Lettuce_1_Sliced_5, agent hand, Bread_1_Sliced_6 [cooked], CounterTop_0, Plate, Knife, CoffeeMachine, Mug [filled]
  Bread_1_Sliced_6, Knife, Lettuce_1_Sliced_5, Plate are in/on CounterTop_1
  Window_1, Pan_2, SaltShaker, Toaster, Microwave, Egg_0 are in/on CounterTop_0
  Mug is in/on CoffeeMachine
  Bread_1_Sliced_7 is inside agent hand"""  
  ...
...
736: 2023/05/05 11:48:03 - 11:48:24: """Goal: Place(CounterTop)
  Visual observation: Mug_1 [dirty], Cabinet_4, Cabinet_5, Cabinet_6, Cabinet_9, Cabinet_11, Sink, CounterTop, Toaster [toggled], Lettuce, CoffeeMachine, Sink_Basin, SaltShaker, Spoon, Knife, Faucet, agent hand
  Spoon, Toaster, SaltShaker, Knife, Mug_1, CoffeeMachine are in/on CounterTop
  Lettuce is inside agent hand
  Speech:
  2023-05-05 11:48:07.992020: hello the apples need to be put in a single cabinet"""  
  ...
737: 2023/05/05 11:48:31 - 11:49:15: """Goal: Pickup(Potato_2)
  Visual observation: SoapBottle_1, Potato_2, Potato_1, Ladle_0, Pot, PepperShaker, DiningTable, Stool, Shelf_4, CounterTop, Lettuce
  Lettuce is in/on CounterTop"""  
  ...
...
741: 2023/05/05 11:51:08 - 11:51:20: """Goal: Place(CounterTop)
  Visual observation: Spatula_1, Cabinet_3, Cabinet_6, Cabinet_10, Cabinet_12, Sink, Drawer, CounterTop, Toaster [toggled], Vase_1, Sink_Basin, ButterKnife, Egg, Spoon, Faucet, Potato_2, Lettuce, agent hand
  Spoon, Toaster, ButterKnife, Potato_2, Lettuce, Spatula_1 are in/on CounterTop
  Egg is inside agent hand"""  
  ...
742: 2023/05/05 11:51:25 - 11:51:25: """Goal: Pickup(Vase_1)
  Visual observation: Spatula_1, Cabinet_3, Cabinet_6, Cabinet_10, Cabinet_12, Sink, Drawer, CounterTop, Toaster [toggled], Vase_1, Sink_Basin, ButterKnife, Egg, Spoon, Faucet, Potato_2, Lettuce
  Spoon, Toaster, Egg, ButterKnife, Potato_2, Lettuce, Spatula_1 are in/on CounterTop"""  
  ...
743: 2023/05/05 11:51:29 - 11:51:29: """Goal: Place(CounterTop)
  Visual observation: Spatula_1, Cabinet_3, Cabinet_6, Cabinet_10, Cabinet_12, Sink, Drawer, CounterTop, Toaster [toggled], Vase_1, Sink_Basin, ButterKnife, Egg, Spoon, Faucet, Potato_2, agent hand, Lettuce
  Spoon, Lettuce, Toaster, Egg, ButterKnife, Potato_2, Spatula_1 are in/on CounterTop
  Vase_1 is inside agent hand"""  
  ...
744: 2023/05/05 11:51:41 - 11:52:11: """Goal: Open(Cabinet_12)
  Visual observation: Cabinet_0, Cabinet_10, Cabinet_12, Drawer, CounterTop, Microwave [toggled], Potato_2, Vase_1, Lettuce, Egg
  Egg, Microwave, Lettuce, Potato_2, Vase_1 are in/on CounterTop
  Speech:
  2023-05-05 11:51:53.837362: check in the shelf next to the fridge"""  
  ...
...
747: 2023/05/05 11:52:33 - 11:53:17: """Goal: Open(Cabinet_8)
  Visual observation: StoveBurner_0, StoveBurner_1, Cabinet_7, Cabinet_8, StoveBurner_2, StoveBurner_3, CounterTop, Window, WineBottle, Pan [dirty], StoveKnob_0 [toggled], StoveKnob_1, StoveKnob_2 [toggled], StoveKnob_3, DishSponge_0, Knife, Potato_2, Vase_1, Lettuce, Egg
  Potato_2, Knife, Vase_1, Lettuce, WineBottle, Egg are in/on CounterTop
  Speech:
  2023-05-05 11:53:05.359115: in the cabinet i have a better view now"""  
  ...
...
756: 2023/05/05 11:54:59 - 11:56:11: """Goal: ToggleOff(Microwave)
  Visual observation: Cabinet_0 [open], Cabinet_1 [open], CounterTop, Microwave [toggled], Cabinet_6 [open], Ladle_2, Potato_2, Vase_1, Lettuce, Egg
  Ladle_2 is in/on Cabinet_6
  Lettuce, Egg, Potato_2, Microwave, Vase_1 are in/on CounterTop
  Speech:
  2023-05-05 11:55:14.780664: check for another apple in the microwave
  2023-05-05 11:56:01.821767: near the fridge and place it in the cabinet"""  
  ...
...
767: 2023/05/05 17:30:14 - 17:30:24: """Goal: Place(CounterTop_0)
  Visual observation: Tomato_1, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_3, Cabinet_4, Cabinet_5, Drawer_17, Sink, HousePlant, Fork, Window, CoffeeMachine, Sink_Basin, SaltShaker_0, Bowl_0 [dirty], Faucet [toggled], agent hand, CounterTop_3, ButterKnife
  Tomato_1, CoffeeMachine, Bowl_0, Faucet, HousePlant, CellPhone_1 are in/on CounterTop_0
  ButterKnife is in/on CounterTop_3
  Mug_1 is inside agent hand"""  
  ...
768: 2023/05/05 17:30:28 - 17:30:28: """Goal: Pickup(Mug_2)
  Visual observation: Mug_2 [filled], Tomato_1, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_3, Cabinet_4, Cabinet_5, Drawer_17, Sink, HousePlant, Fork, Window, CoffeeMachine, Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], CounterTop_3, ButterKnife
  HousePlant, CellPhone_1, Mug_1, Bowl_0, Tomato_1, Faucet, CoffeeMachine are in/on CounterTop_0
  ButterKnife is in/on CounterTop_3"""  
  ...
769: 2023/05/05 17:30:33 - 17:30:33: """Goal: Pour(Sink)
  Visual observation: Mug_2 [filled], Tomato_1, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_3, Cabinet_4, Cabinet_5, Drawer_17, Sink, HousePlant, Fork, Window, CoffeeMachine, Sink_Basin, SaltShaker_0, Bowl_0 [dirty], Faucet [toggled], agent hand, CounterTop_3, ButterKnife
  HousePlant, CellPhone_1, Mug_1, Tomato_1, Faucet, Bowl_0, CoffeeMachine are in/on CounterTop_0
  Mug_2 is inside agent hand
  ButterKnife is in/on CounterTop_3
  Fork, SaltShaker_1, SaltShaker_0 are in/on Sink_Basin"""  
  ...
770: 2023/05/05 17:30:36 - 17:30:36: """Goal: Place(CoffeeMachine)
  Visual observation: Mug_2, Tomato_1, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_3, Cabinet_4, Cabinet_5, Drawer_17, Sink, HousePlant, Fork, Window, CoffeeMachine, Sink_Basin, SaltShaker_0, Bowl_0 [dirty], Faucet [toggled], agent hand, CounterTop_3, ButterKnife
  HousePlant, CellPhone_1, Mug_1, Tomato_1, Faucet, Bowl_0, CoffeeMachine are in/on CounterTop_0
  Mug_2 is inside agent hand
  ButterKnife is in/on CounterTop_3
  Fork, SaltShaker_1, SaltShaker_0 are in/on Sink_Basin"""  
  ...
771: 2023/05/05 17:30:41 - 17:30:41: """Goal: ToggleOn(CoffeeMachine)
  Visual observation: Mug_2, Tomato_1, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_3, Cabinet_4, Cabinet_5, Drawer_17, Sink, HousePlant, Fork, Window, CoffeeMachine, Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], CounterTop_3, ButterKnife
  HousePlant, CellPhone_1, Mug_1, Bowl_0, Tomato_1, Faucet, CoffeeMachine, Mug_2 are in/on CounterTop_0
  Egg_0, Fork, SaltShaker_1, SaltShaker_0 are in/on Sink_Basin
  ButterKnife is in/on CounterTop_3
  Mug_2 is in/on CoffeeMachine"""  
  ...
772: 2023/05/05 17:30:53 - 17:31:28: """Goal: Pickup(Bread_0_Sliced_7)
  Visual observation: Pot_0, CoffeeMachine [toggled], Mug_2, CounterTop_0, Mug_1 [filled], CounterTop_3, ButterKnife
  Mug_1, CoffeeMachine, Mug_2 are in/on CounterTop_0
  Pot_0, ButterKnife are in/on CounterTop_3
  Mug_2 is in/on CoffeeMachine
  Speech:
  2023-05-05 17:31:12.454624: Next, please make a sandwich. Could you start with toasting 2 slices of bread?"""  
  ...
...
782: 2023/05/05 17:32:40 - 17:32:53: """Goal: Slice(Tomato_1)
  Visual observation: Tomato_1, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_4, Cabinet_5, Cabinet_6, Sink, HousePlant, Fork, Window, CoffeeMachine [toggled], Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], Plate, Bread_0_Sliced_7 [cooked], Bread_0_Sliced_6 [cooked], Mug_2, CounterTop_1, agent hand, ButterKnife
  Plate, Bread_0_Sliced_7, Bread_0_Sliced_6 are in/on CounterTop_1
  Bread_0_Sliced_6, Bread_0_Sliced_7 are in/on Plate
  CoffeeMachine, Mug_2, HousePlant, Faucet, Mug_1, Tomato_1, Bowl_0, CellPhone_1 are in/on CounterTop_0
  Egg_0, SaltShaker_0, SaltShaker_1, Fork are in/on Sink_Basin
  ButterKnife is inside agent hand
  Mug_2 is in/on CoffeeMachine"""  
  ...
783: 2023/05/05 17:32:57 - 17:32:57: """Goal: Place(CounterTop_0)
  Visual observation: Tomato_1_Sliced_5, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_4, Cabinet_5, Cabinet_6, Sink, HousePlant, Fork, Window, CoffeeMachine [toggled], Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], Plate, Bread_0_Sliced_7 [cooked], Bread_0_Sliced_6 [cooked], Mug_2, CounterTop_1, agent hand, ButterKnife
  Mug_1, Bowl_0, CellPhone_1, Tomato_1_Sliced_1, CoffeeMachine, Tomato_1_Sliced_2, HousePlant, Tomato_1_Sliced_5, Tomato_1_Sliced_0, Mug_2, Tomato_1_Sliced_4, Faucet, Tomato_1_Sliced_3 are in/on CounterTop_0
  Fork, Egg_0, SaltShaker_1, SaltShaker_0 are in/on Sink_Basin
  Bread_0_Sliced_6, Bread_0_Sliced_7 are in/on Plate
  Bread_0_Sliced_6, Plate, Bread_0_Sliced_7 are in/on CounterTop_1
  ButterKnife is inside agent hand
  Mug_2 is in/on CoffeeMachine"""  
  ...
784: 2023/05/05 17:33:00 - 17:33:17: """Goal: Pickup(Tomato_1_Sliced_1)
  Visual observation: Tomato_1_Sliced_5, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_4, Cabinet_5, Cabinet_6, Sink, HousePlant, Fork, Window, CoffeeMachine [toggled], Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], Mug_2, ButterKnife
  Mug_1, Bowl_0, CellPhone_1, Tomato_1_Sliced_1, CoffeeMachine, Tomato_1_Sliced_2, HousePlant, Tomato_1_Sliced_5, Tomato_1_Sliced_0, Mug_2, Tomato_1_Sliced_4, Faucet, Tomato_1_Sliced_3, ButterKnife are in/on CounterTop_0
  Fork, Egg_0, SaltShaker_1, SaltShaker_0 are in/on Sink_Basin
  Mug_2 is in/on CoffeeMachine"""  
  ...
785: 2023/05/05 17:33:20 - 17:33:20: """Goal: Place(Bowl_0)
  Visual observation: Tomato_1_Sliced_5, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_4, Cabinet_5, Cabinet_6, Sink, HousePlant, Fork, Window, CoffeeMachine [toggled], Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], agent hand, Mug_2, ButterKnife
  Mug_1, Bowl_0, CellPhone_1, CoffeeMachine, Tomato_1_Sliced_2, HousePlant, Tomato_1_Sliced_5, ButterKnife, Tomato_1_Sliced_0, Tomato_1_Sliced_4, Faucet, Tomato_1_Sliced_3, Mug_2 are in/on CounterTop_0
  Fork, Egg_0, SaltShaker_1, SaltShaker_0 are in/on Sink_Basin
  Mug_2 is in/on CoffeeMachine
  Tomato_1_Sliced_1 is inside agent hand"""  
  ...
786: 2023/05/05 17:33:25 - 17:33:25: """Goal: Pickup(Tomato_1_Sliced_2)
  Visual observation: Tomato_1_Sliced_5, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_4, Cabinet_5, Cabinet_6, Sink, HousePlant, Fork, Window, CoffeeMachine [toggled], Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], Mug_2, ButterKnife
  Mug_1, Bowl_0, CellPhone_1, Tomato_1_Sliced_1, CoffeeMachine, Tomato_1_Sliced_2, HousePlant, Tomato_1_Sliced_5, Tomato_1_Sliced_0, Mug_2, Tomato_1_Sliced_4, Faucet, Tomato_1_Sliced_3, ButterKnife are in/on CounterTop_0
  Fork, Egg_0, SaltShaker_1, SaltShaker_0 are in/on Sink_Basin
  Tomato_1_Sliced_1 is in/on Bowl_0
  Mug_2 is in/on CoffeeMachine"""  
  ...
787: 2023/05/05 17:33:27 - 17:33:30: """Goal: Place(Bowl_0)
  Visual observation: Tomato_1_Sliced_5, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_4, Cabinet_5, Cabinet_6, Sink, HousePlant, Fork, Window, CoffeeMachine [toggled], Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], agent hand, Mug_2, ButterKnife
  Mug_1, Bowl_0, CellPhone_1, Tomato_1_Sliced_1, CoffeeMachine, HousePlant, Tomato_1_Sliced_5, ButterKnife, Tomato_1_Sliced_0, Tomato_1_Sliced_4, Faucet, Tomato_1_Sliced_3, Mug_2 are in/on CounterTop_0
  Tomato_1_Sliced_2 is inside agent hand
  Fork, Egg_0, SaltShaker_1, SaltShaker_0 are in/on Sink_Basin
  Tomato_1_Sliced_1 is in/on Bowl_0
  Mug_2 is in/on CoffeeMachine
  Speech:
  2023-05-05 17:33:27.134052: add to the plate"""  
  ...
788: 2023/05/05 17:33:34 - 17:33:34: """Goal: Pickup(Bowl_0)
  Visual observation: Tomato_1_Sliced_5, Tomato_1_Sliced_4, Tomato_1_Sliced_3, Tomato_1_Sliced_2, Tomato_1_Sliced_1, Tomato_1_Sliced_0, SaltShaker_1, CellPhone_1, Mug_1 [filled], Drawer_1, Drawer_6, CounterTop_0, Cabinet_4, Cabinet_5, Cabinet_6, Sink, HousePlant, Fork, Window, CoffeeMachine [toggled], Sink_Basin, SaltShaker_0, Egg_0, Bowl_0 [dirty], Faucet [toggled], Mug_2, ButterKnife
  Mug_1, Bowl_0, CellPhone_1, Tomato_1_Sliced_1, CoffeeMachine, Tomato_1_Sliced_2, HousePlant, Tomato_1_Sliced_5, Tomato_1_Sliced_0, Mug_2, Tomato_1_Sliced_4, Faucet, Tomato_1_Sliced_3, ButterKnife are in/on CounterTop_0
  Fork, Egg_0, SaltShaker_0, SaltShaker_1 are in/on Sink_Basin
  Tomato_1_Sliced_2, Tomato_1_Sliced_1 are in/on Bowl_0
  Mug_2 is in/on CoffeeMachine"""  
  ...
789: 2023/05/05 17:33:35 - 17:33:52: """Goal: Place(CounterTop_1)
  Visual observation: Tomato_1_Sliced_2, Tomato_1_Sliced_1, DishSponge_2, Spatula_1, Drawer_5, Drawer_7, CounterTop_1, Drawer_8, Drawer_10, Drawer_11, Drawer_13, Cabinet_12, Drawer_16, Drawer_18, Drawer_19, Drawer_21, Drawer_22, Drawer_23, Drawer_25, Mirror [dirty], Plate, Pan [dirty], Toaster [toggled], Microwave, Bowl_0 [dirty], CoffeeMachine [toggled], Mug_2, CounterTop_0, Mug_1 [filled], ButterKnife, agent hand
  CoffeeMachine, ButterKnife, Mug_2, Mug_1 are in/on CounterTop_0
  Spatula_1, DishSponge_2, Plate, Microwave, Toaster, Pan are in/on CounterTop_1
  Bowl_0 is inside agent hand
  Tomato_1_Sliced_1, Tomato_1_Sliced_2 are in/on Bowl_0
  Mug_2 is in/on CoffeeMachine"""  
  ...
...
807: 2023/05/07 15:25:49 - 15:26:34: """Goal: Place(CoffeeMachine)
  Visual observation: Spoon_1, Egg_1, Sink, CounterTop_0, Cabinet_3, Cabinet_6, Cabinet_7, Drawer_0, Cup_0, Window_0, Spatula_0, Knife, Sink_Basin, CoffeeMachine [toggled], Mug_0, Faucet [toggled], Statue_0, agent hand
  CoffeeMachine, Cup_0, Egg_1, Sink, Knife, Statue_0 are in/on CounterTop_0
  Faucet, Spoon_1 are in/on Sink
  Mug_0 is inside agent hand
  Speech:
  2023-05-07 15:26:16.508638: The coffee maker is next to the sink"""  
  ...
808: 2023/05/07 15:26:38 - 15:26:47: """Goal: LookDown()
  Visual observation: Cabinet_0, Cabinet_10, Cabinet_11, Window_0, CoffeeMachine [toggled], Mug_0 [filled]
  Mug_0 is in/on CoffeeMachine
  Speech:
  2023-05-07 15:26:45.118023: Finished"""  
  ...
...
]

>>> answer("prepare breakfast. and cook 1 slice(s) of potato and serve on a plate. and clean all the cookwares. and clean all the tablewares. and water the plant. and make a plate of toast.")

