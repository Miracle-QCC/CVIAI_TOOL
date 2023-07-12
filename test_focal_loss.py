import torch
device = 'cpu'
from torch.nn import functional as F

def focalloss(inputs, targets, alpha = 0.6, gamma=2):
    alpha = torch.tensor([alpha, 1 - alpha]).to(device)
    BCE_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
    targets = targets.type(torch.long)
    at = alpha.gather(0, targets.data.view(-1))
    pt = torch.exp(-BCE_loss)
    F_loss = at * (1 - pt) ** gamma * BCE_loss
    return F_loss.mean()


inputs = torch.tensor([0.5])
targets = torch.tensor([2.0])

focalloss(inputs,targets)