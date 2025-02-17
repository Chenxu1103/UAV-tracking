import os
import torch
import torch.nn as nn

class ViT(nn.Module):
    def __init__(self):
        super(ViT, self).__init__()
        self.feature = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.fc = nn.Linear(64, 4)

    def forward(self, x):
        x = self.feature(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

class ProContEXTNetwork(nn.Module):
    def __init__(self, weight_path):
        super(ProContEXTNetwork, self).__init__()
        self.backbone = ViT()
        self.load_weights(weight_path)

    def load_weights(self, weight_path):
        if os.path.exists(weight_path):
            state_dict = torch.load(weight_path)
            self.load_state_dict(state_dict, strict=False)
            print(f"Successfully loaded weights from {weight_path}")
        else:
            print(f"Failed to load weights: File {weight_path} does not exist")

    def forward(self, x):
        features = self.backbone(x)
        return features
