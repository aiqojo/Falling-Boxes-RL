import gym
from stable_baselines3 import PPO, DQN, A2C
import os
import time
from dojenv import dojEnv

load = False

models_dir = f"models/DojB-PPO5"
logdir = f"logs/DojB-PPO5"

models_path = f"{models_dir}/1025000.zip"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = dojEnv()
env.reset()

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
# model = PPO.load(models_path, env = env)
TIMESTEPS = 25000
for i in range(1, 100000):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")

    if load:
        env_load = dojEnv()
        env_load.reset()

        load_path = f"{models_dir}/{TIMESTEPS*i}.zip"

        model = PPO.load(load_path, env=env_load)

        reward_array = []

        episodes = 4
        for ep in range(episodes):
            obs = env_load.reset()
            done = False
            while not done:
                time.sleep(0.02)
                env_load.render()
                action, _ = model.predict(obs)
                obs, reward, done, info = env_load.step(action)
                # print(np.fliplr(np.rot90(m=obs, k=3)))
                print(reward)
            reward_array += [reward]

        env_load.close()


env.close()
