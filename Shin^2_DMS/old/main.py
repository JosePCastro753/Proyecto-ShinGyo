"""
Proyecto Shin DMS
@author: Jose Pablo Castro
@author: David Jimenez
"""
import numpy as np
import os
import argparse
import pandas as pd
import Enviroment as envr
from dqn_agent import Agent

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
class Environment(object):

    def __init__(self, arguments):
        self.env = envr.Scenario()
        self.episodes_number = arguments['episode_number']
        self.render = arguments['render']
        self.test = arguments['test']

    def run(self, agent_completar_lotes, agent_meter_urgentes_1 , agent_meter_urgentes_2, agent_establecer_buffer, agent_establecer_drum, rewards_file):
        max_score = -10000
        state = self.env.reset()
        state = np.array(state)
        state = state.ravel()
        done = True
        reward_all = 0


        for episode_num in range(self.episodes_number):
            actions = []

            action_completar_lotes = agent_completar_lotes.greedy_actor(state)
            action_meter_urgentes_1 = agent_meter_urgentes_1.greedy_actor(state)
            action_meter_urgentes_2 = agent_meter_urgentes_2.greedy_actor(state)
            action_establecer_buffer = agent_establecer_buffer.greedy_actor(state)
            action_establecer_drum = agent_establecer_drum.greedy_actor(state)

            actions.append(action_completar_lotes)
            actions.append(action_meter_urgentes_1)
            actions.append(action_meter_urgentes_2)
            actions.append(action_establecer_buffer)
            actions.append(action_establecer_drum)

            reward = self.env.step(action_completar_lotes, action_meter_urgentes_1, action_meter_urgentes_2, action_establecer_buffer, action_establecer_drum)


            next_state = self.env.reset()
            next_state = np.array(next_state)
            next_state = next_state.ravel()

            #if not self.test:
            x = True
            if x == True:
                agent_completar_lotes.observe((state,actions, reward, next_state, done))
                agent_meter_urgentes_1.observe((state,actions, reward, next_state, done))
                agent_meter_urgentes_2.observe((state,actions, reward, next_state, done))
                agent_establecer_buffer.observe((state,actions, reward, next_state, done))
                agent_establecer_drum.observe((state,actions, reward, next_state, done))

                agent_completar_lotes.decay_epsilon()
                agent_meter_urgentes_1.decay_epsilon()
                agent_meter_urgentes_2.decay_epsilon()
                agent_establecer_buffer.decay_epsilon()
                agent_establecer_drum.decay_epsilon()

                agent_completar_lotes.replay()
                agent_meter_urgentes_1.replay()
                agent_meter_urgentes_2.replay()
                agent_establecer_buffer.replay()
                agent_establecer_drum.replay()

                agent_completar_lotes.update_target_model()
                agent_meter_urgentes_1.update_target_model()
                agent_meter_urgentes_2.update_target_model()
                agent_establecer_buffer.update_target_model()
                agent_establecer_drum.update_target_model()

            state = next_state
            reward_all += reward
            self.resumen = self.env.info()
            list = [{'time': episode_num, 'score': reward, 'escenario': self.resumen[0], 'completar_lotes': action_completar_lotes,
                     'meter_urgentes_1': action_meter_urgentes_1, 'meter_urgentes_2': action_meter_urgentes_2,
                     'establecer_buffer': action_establecer_buffer, 'establecer_drum': action_establecer_drum,
                     'resultados': self.resumen[2]}]
            if self.render:
                print(self.resumen)
            df = pd.DataFrame(list)
            df.to_csv(rewards_file, mode='a', header=False, index=False)
            if not self.test:
                if episode_num % 100 == 0:
                    if reward_all > max_score:
                        agent_completar_lotes.brain.save_model()
                        agent_meter_urgentes_1.brain.save_model()
                        agent_meter_urgentes_2.brain.save_model()
                        agent_establecer_buffer.brain.save_model()
                        agent_establecer_drum.brain.save_model()
                        max_score = reward_all

seguro = 569895
if seguro == 569895:

    parser = argparse.ArgumentParser()
    # Parametros DQN
    parser.add_argument('-e', '--episode-number', default=100, type=int, help='Number of episodes')
    parser.add_argument('-l', '--learning-rate', default=0.00005, type=float, help='Learning rate')
    parser.add_argument('-op', '--optimizer', choices=['Adam', 'RMSProp'], default='RMSProp',
                        help='Optimization method')
    parser.add_argument('-m', '--memory-capacity', default=1000000, type=int, help='Memory capacity')
    parser.add_argument('-b', '--batch-size', default=64, type=int, help='Batch size')
    parser.add_argument('-ps', '--prioritization-scale', default=0.5, type=float, help='Scale for prioritization')
    parser.add_argument('-t', '--target-frequency', default=10000, type=int,
                        help='Number of steps between the updates of target network')
    parser.add_argument('-x', '--maximum-exploration', default=100000, type=int, help='Maximum exploration step')
    parser.add_argument('-rs', '--replay-steps', default=4, type=float, help='Steps between updating the network')
    parser.add_argument('-nn', '--number-nodes', default=256, type=int, help='Number of nodes in each layer of NN')
    parser.add_argument('-tt', '--target-type', choices=['DQN', 'DDQN'], default='DDQN')
    parser.add_argument('-mt', '--memory', choices=['UER', 'PER'], default='PER')
    parser.add_argument('-pl', '--pmax-random-movesrioritization-scale', default=0.5, type=float, help='Scale for prioritization')
    parser.add_argument('-du', '--dueling', action='store_true', help='Enable Dueling architecture if "store_false" ')

    parser.add_argument('-gn', '--gpu-num', default='3', type=str, help='Number of GPU to use')
    parser.add_argument('-test', '--test', action='store_true', help='Enable the test phase if "store_false"')

    # Parametros simulacion
    parser.add_argument('-r', '--render', action='store_false', help='Activa la vizualizacion si "store_false"')
    args = vars(parser.parse_args())
    os.environ['CUDA_VISIBLE_DEVICES'] = args['gpu_num']
    state_size = 9
    action_space_binary = 2
    action_space_box = 10001
    rewards_file = "record.csv"
    env = Environment(args)

    agent_completar_lotes = Agent(state_size, action_space_binary, 0, 'b1.h5', args)
    agent_meter_urgentes_1 = Agent(state_size, action_space_binary, 1, 'b2.h5', args)
    agent_meter_urgentes_2 = Agent(state_size, action_space_binary, 2, 'b3.h5', args)
    agent_establecer_buffer = Agent(state_size, action_space_box, 3, 'b4.h5', args)
    agent_establecer_drum = Agent(state_size, action_space_box, 4, 'b5.h5', args)

    env.run(agent_completar_lotes, agent_meter_urgentes_1 , agent_meter_urgentes_2, agent_establecer_buffer, agent_establecer_drum, rewards_file)
