import torch
from torch import nn
import torch.nn.functional as F

from settings import MctsSettings, NetworkSettings


class Block(nn.Module):
    """Basic redisual block."""

    def __init__(self,
                 network_settings: NetworkSettings
                 ) -> None:
        super().__init__()

        self.conv_block1 = nn.Sequential(
            nn.Conv2d(
                in_channels=network_settings.channels_n,
                out_channels=network_settings.channels_n,
                kernel_size=3,
                stride=1,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(
                num_features=network_settings.channels_n
            ),
            nn.ReLU(),
        )

        self.conv_block2 = nn.Sequential(
            nn.Conv2d(
                in_channels=network_settings.channels_n,
                out_channels=network_settings.channels_n,
                kernel_size=3,
                stride=1,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(
                num_features=network_settings.channels_n
            ),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        out = self.conv_block1(x)
        out = self.conv_block2(out)
        out += residual
        out = F.relu(out)
        return out


class Network(nn.Module):

    def __init__(self,
                 mcts_settings: MctsSettings,
                 network_settings: NetworkSettings
                 ) -> None:
        super().__init__()

        self.conv_block = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=network_settings.channels_n,
                kernel_size=3,
                stride=1,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(
                num_features=network_settings.channels_n,
            ),
            nn.ReLU()
        )

        self.blocks = nn.Sequential(
            *[Block(network_settings)
              for _ in range(network_settings.blocks_n)]
        )

        self.head = nn.Sequential(
            nn.Conv2d(
                in_channels=network_settings.channels_n,
                out_channels=2,
                kernel_size=1,
                stride=1,
                bias=False,
            ),
            nn.BatchNorm2d(
                num_features=2
            ),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(
                in_features=2 * mcts_settings.dim * mcts_settings.dim,
                out_features=mcts_settings.n_actions,
            ),
        )
        if network_settings.is_softmax:
            self.head.add_module('softmax', nn.Softmax(dim=1))


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.conv_block(x)
        out = self.blocks(out)
        out = self.head(out)
        return out




