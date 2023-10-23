import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models.resnet import ResNet18_Weights
import torchvision.models as models
import os



# Defina transformações para pré-processar as imagens
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Determina o caminho do diretório onde o script atual reside
script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho relativo a partir do diretório do script
dataset_path = os.path.join(script_dir, '', 'datasets', 'vegetacao')

train_data = datasets.ImageFolder(dataset_path, transform=transform)


train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

# Utilize um modelo pré-treinado e ajuste a última camada
#versao deprecada
# model = models.resnet18(pretrained=True)

#versao nova
model = models.resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)


model.fc = nn.Linear(model.fc.in_features, 2)  # Supondo que temos 2 classes: Lixo e Não-Lixo

# Função de perda e otimizador
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Treinamento do modelo
num_epochs = 10
for epoch in range(num_epochs):
    for inputs, labels in train_loader:
        # Forward pass
        outputs = model(inputs)

        # Calcule a perda
        loss = criterion(outputs, labels)

        # Backward pass e otimização
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
