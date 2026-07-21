import torch
import torch.nn as nn

# A tiny neural network: 2 inputs -> 1 hidden neuron -> 1 output
class TinyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(2, 1)   # 2 inputs -> 1 hidden neuron
        self.output = nn.Linear(1, 1)   # 1 hidden -> 1 output

    def forward(self, x):
        x = torch.relu(self.hidden(x))   # forward pass through hidden layer
        x = self.output(x)                # forward pass through output layer
        return x


model = TinyNet()

# Sample input and target
x = torch.tensor([[2.0, 3.0]])
target = torch.tensor([[10.0]])

# Loss function
loss_fn = nn.MSELoss()

# Optimizer - handles the gradient descent step for us
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# One training step
prediction = model(x)               # forward pass
loss = loss_fn(prediction, target)   # calculate loss
print(f"Prediction: {prediction.item():.2f}, Loss: {loss.item():.2f}")

optimizer.zero_grad()   # clear old gradients
loss.backward()          # backpropagation - calculate gradients
optimizer.step()          # gradient descent - update weights

prediction2 = model(x)
loss2 = loss_fn(prediction2, target)
print(f"After 1 step - Prediction: {prediction2.item():.2f}, Loss: {loss2.item():.2f}")