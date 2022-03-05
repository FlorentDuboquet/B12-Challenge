from sdk import *
import sys
from time import time
import numpy as np




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
    #Compute distance to checkpoint

    power =75

    # ApplyForce(car.id, team_id, [argument of next_checkpoint.pos - car.pos], 100)
    # (tip: that argument can be computed with atan2)
    return ForceTowards(car.id, team_id, next_checkpoint.pos, power )

  def order_for_car_to_target_other_player(car: Car, target_car: Car) -> PlayerOrder:
    if not car.boost_used:
      # The boost is still free to use, let's use it!
      return UseBoost(car.id, team_id)
    return ForceTowards(car.id, team_id, target_car.pos, 75)

  def defend_planet (car: Car, planet, other_cars, ally_car) :
    power = 100
    attaque = True
    target = planet.pos
    log.info(str(ally_car.next_checkpoint(game_state).id))
    log.info(str(planet.id))

    #Clear planet for ally
    if ally_car.next_checkpoint(game_state).id == planet.id:
      log.info("Clear planet")
      distance_planet_ally = abs((ally_car.pos.real - planet.pos.real) * np.cos(ally_car.pos.imag - planet.pos.imag))
      if distance_planet_ally < 100:
        dist1 = abs((other_cars[1].pos.real - planet.pos.real) * np.cos(other_cars[1].pos.imag - planet.pos.imag))
        dist0 = abs((other_cars[0].pos.real - planet.pos.real) * np.cos(other_cars[0].pos.imag - planet.pos.imag))
        if dist1 < dist0:
          car_to_target = other_cars[1]
        else:
          car_to_target = other_cars[0]
        return ForceTowards(car.id, team_id, car_to_target.pos, power)
    #Annoy the other
    if other_cars[0].next_checkpoint(game_state).id == planet.id & other_cars[1].next_checkpoint(game_state).id != planet.id:
      car_to_target = other_cars[0]
    elif other_cars[0].next_checkpoint(game_state).id != planet.id & other_cars[1].next_checkpoint(game_state).id == planet.id:
      car_to_target = other_cars[1]
    elif other_cars[0].next_checkpoint(game_state).id != planet.id & other_cars[1].next_checkpoint(game_state).id != planet.id:
      attaque = False

    else :
      dist1 = abs((other_cars[1].pos.real - planet.pos.real)*np.cos(other_cars[1].pos.imag - planet.pos.imag))
      dist0 = abs((other_cars[0].pos.real - planet.pos.real)*np.cos(other_cars[0].pos.imag - planet.pos.imag))
      if dist1 < dist0 :
        car_to_target=other_cars[1]
      else :
        car_to_target=other_cars[0]


    distance_planet = abs((car.pos.real - planet.pos.real)*np.cos(car.pos.imag - planet.pos.imag))

    if attaque :
      log.info("Dans attaque")

      intersection_point = complex(int((car_to_target.pos.real + planet.pos.real)/2),int((car_to_target.pos.imag + planet.pos.imag)/2))
      distance_planet_car_to_target = abs((car_to_target.pos.real - planet.pos.real)*np.cos(car_to_target.pos.imag - planet.pos.imag))
      log.info(str(intersection_point))
      log.info(str(distance_planet_car_to_target))

      if distance_planet > 100 :
          if distance_planet > 200:
            power = 100
          else :
            power = int(distance_planet/2)
          target = planet.pos
          return ForceTowards(car.id, team_id, target, power)
      else :
          if distance_planet_car_to_target < 42:

            log.info('Attacking')
            #Estimer position du ship avec sa vitesse
            power = 100
            target = car_to_target.pos + car_to_target.speed*0.05
            return ForceTowards(car.id, team_id, target, power)
          elif distance_planet_car_to_target < 2*42:

            log.info('Prepare to attack')
            #Prepare to attack
            power = 100
            target = intersection_point
            return ForceTowards(car.id, team_id, target, power)
          else :

            log.info('Staying close to planet')
            power = 75
            target = planet.pos
            return ForceTowards(car.id, team_id, target, power)

    else :
      log.error("No one is attacking, staying close to planet")

      power = 100
      return ForceTowards(car.id, team_id, planet.pos, power)












  # Retrieve the list of your ships. You can always assume it will be of length 2
  my_cars = [car for car in game_state.cars if car.team_id == team_id]
  other_cars = [car for car in game_state.cars if car.team_id != team_id]
  target_car = 77
  if game_state.is_started:
    # The game has started. Deciding what to do with our two ships

    #Target the smaller car
    if target_car == 77 :
      if other_cars[0].mass >= other_cars[1].mass :
        target_car = other_cars[1]
      else :
        target_car = other_cars[0]

    planet_to_defend = game_state.checkpoints[2]

    log.info("I'm creating my order")
    order = OrderForEachCar(defend_planet (my_cars[0], planet_to_defend, other_cars, my_cars[1] ), order_for_car(my_cars[1]))

  else:
    # Game has not yet started. It is the only place where we can (and must!) set the masses for the ships.

    '''DECISION POUR LES MASSES'''
    order = SetCarMasses(team_id, my_cars[0].id, my_cars[1].id,13, 7)


  time_taken = time() - now
  # Logging how much time it took.
  log.info(f"It took {time_taken * 1000000} micro seconds to complete.")
  return order

# Starting the game loop, you can leave this line as is.
Runner(team_id, game_loop).run()
