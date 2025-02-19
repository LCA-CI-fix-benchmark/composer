# 🎰 Stochastic Depth (Sample)

[\[How to Use\]](#how-to-use) - [\[Suggested Hyperparameters\]](#suggested-hyperparameters) - [\[Technical Details\]](#technical-details) - [\[Attribution\]](#attribution) - [\[API Reference\]](#api-reference)

 `Computer Vision`

 Sample-wise stochastic depth is a regularization technique for networks with residual connections that probabilistically drops samples after the transformation function in each residual block. This means that different samples go through different combinations of blocks.

## How to Use

### Functional Interface

<!--pytest.mark.gpu-->
<!--
```python
from torch.utils.data import DataLoader
from tests.common import RandomImageDataset

train_dataloader = DataLoader(RandomImageDataset(size=2), batch_size=2)
```
-->
<!--pytest-codeblocks:cont-->
```python
# Run the Stochastic Depth algorithm directly on the model using the Composer functional API

import torch
import torch.nn.functional as F

import composer.functional as cf
from composer.models import composer_resnet

# Training

# Stochastic depth can only be run on ResNet-50/101/152
model = composer_resnet('resnet50')

opt = torch.optim.Adam(model.parameters())

cf.apply_stochastic_depth(
    model,
    target_layer_name='ResNetBottleneck',
    stochastic_method='sample',
    drop_rate=0.2,
    drop_distribution='linear'
)

loss_fn = F.cross_entropy
model.train()

for epoch in range(1):
    for X, y in train_dataloader:
        y_hat = model([X, y])
        loss = loss_fn(y_hat, y)
        loss.backward()
        opt.step()
        opt.zero_grad()
        break
```

### Composer Trainer

<!--pytest.mark.gpu-->
<!--
```python
from torch.utils.data import DataLoader
from tests.common import RandomImageDataset

train_dataloader = DataLoader(RandomImageDataset(size=2), batch_size=2)
eval_dataloader = DataLoader(RandomImageDataset(size=2), batch_size=2)
```
-->
<!--pytest-codeblocks:cont-->
```python
# Instantiate the algorithm and pass it into the Trainer
# The trainer will automatically run it at the appropriate point in the training loop

from composer.algorithms import StochasticDepth
from composer.models import composer_resnet
from composer.trainer import Trainer

# Train model

# Stochastic depth can only be run on ResNet-50/101/152
model = composer_resnet('resnet50')

stochastic_depth = StochasticDepth(
    target_layer_name='ResNetBottleneck',
    stochastic_method='sample',
    drop_rate=0.2,
    drop_distribution='linear'
)

trainer = Trainer(
    model=model,
    train_dataloader=train_dataloader,
    eval_dataloader=eval_dataloader,
    max_duration='1ep',
    algorithms=[stochastic_depth]
)

trainer.fit()
```

### Implementation Details

The Composer implementation of Stochastic Depth uses model surgery to replace residual bottleneck blocks with analogous stochastic versions. When training, samples are dropped after the transformation function in a residual block by multiplying the batch by a binary vector. The binary vector is generated by sampling independent Bernoulli distributions with probability (1 - `drop_rate`). After the samples are dropped, the skip connection is added as usual. During inference, no samples are dropped, but the batch of samples is scaled by (1 - `drop_rate`) to compensate for the drop frequency when training.

## Suggested Hyperparameters

We observe that `drop_rate=0.1` and `drop_distribution=linear` yield maximum accuracy improvements on both ResNet-50 and ResNet-101.

## Technical Details

For both ResNet-50 and ResNet-101 on ImageNet, we measure a +0.4% absolute accuracy improvement when using `drop_rate=0.1` and `drop_distribution=linear`. The training wall-clock time is approximately 5% longer when using sample-wise stochastic depth.

## Attribution

[Deep Networks with Stochastic Depth](https://arxiv.org/abs/1603.09382) by Gao Huang, Yu Sun, Zhuang Liu, Daniel Sedra, and Killian Weinberger. Published in ECCV in 2016.

[EfficientNet model in the TPU Github repository](https://github.com/tensorflow/tpu/tree/master/models/official/efficientnet) from Google

[EfficientNet model in gen-efficientnet-pytorch Github repository](https://github.com/rwightman/gen-efficientnet-pytorch) by Ross Wightman

## API Reference

**Algorithm class:** {class}`composer.algorithms.StochasticDepth`

**Functional:** {func}`composer.functional.apply_stochastic_depth`
