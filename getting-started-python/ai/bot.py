from sdk import *
import sys
from time import time




# Reading my team id from the command line args
team_id = int(sys.argv[1])

def game_loop(game_state: GameState, game_time: int, log: Logger) -> PlayerOrder:
  now = time()
  # Logging something using the logger. This will show up in game logs on the platform
  log.info(f"Received the game state. My team is {team_id}")

  def order_for_car(car: Car) -> PlayerOrder:
    if not car.boost_used:
      # The boost is still free to use, let's use it!
      return UseBoost(car.id, team_id)
    next_checkpoint = car.next_checkpoint(game_state)
    # ApplyForce(car.id, team_id, [argument of next_checkpoint.pos - car.pos], 100)
    # (tip: that argument can be computed with atan2)
    return ForceTowards(car.id, team_id, next_checkpoint.pos, 100)

  def order_for_car_to_target_other_player(car: Car, target_car: Car) -> PlayerOrder:
    if not car.boost_used:
      # The boost is still free to use, let's use it!
      return UseBoost(car.id, team_id)
    return ForceTowards(car.id, team_id, target_car.pos, 100)









  # Retrieve the list of your ships. You can always assume it will be of length 2
  my_cars = [car for car in game_state.cars if car.team_id == team_id]
  other_cars = [car for car in game_state.cars if car.team_id != team_id]
  target_car = 77
  if game_state.is_started:
    # The game has started. Deciding what to do with our two ships
    if target_car == 77 :
      if other_cars[0].mass >= other_cars[1].mass :
        target_car = other_cars[1]
      else :
        target_car = other_cars[0]
        log.info(type(target_car))
    log.info("I'm creating my order")
    order = OrderForEachCar(order_for_car_to_target_other_player(my_cars[0],target_car), order_for_car(my_cars[1]))

  else:
    # Game has not yet started. It is the only place where we can (and must!) set the masses for the ships.

    '''DECISION POUR LES MASSES'''
    order = SetCarMasses(team_id, my_cars[0].id, my_cars[1].id, 15, 5)


  time_taken = time() - now
  # Logging how much time it took.
  log.info(f"It took {time_taken * 1000000} micro seconds to complete.")
  return order

# Starting the game loop, you can leave this line as is.
Runner(team_id, game_loop).run()
