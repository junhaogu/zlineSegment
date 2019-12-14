# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JxBgWSEqWe63cglskQJJE8RudhMEgrYg
"""
import torch
from torch.utils.data import DataLoader, TensorDataset
def k_cross_data_split(sample_data, mask, batch_size,fold,kf):
  foldsize=sample_data.shape[0]//kf
  train_image=torch.zeros([1,3,256,512]).type(torch.float)
  train_mask=torch.zeros([1,1,256,512]).type(torch.float)
  for j in range(kf):
    if fold!=j:
      if j!=kf-1:
        train_image=torch.cat((train_image,sample_data[j*foldsize:(j+1)*foldsize,:,:,:]),0)
        train_mask=torch.cat((train_mask,mask[j*foldsize:(j+1)*foldsize,:,:,:]),0)
      else:
        train_image=torch.cat((train_image,sample_data[j*foldsize:,:,:,:]),0)
        train_mask=torch.cat((train_mask,mask[j*foldsize:,:,:,:]),0)
  if fold!=kf-1:
    test_image=sample_data[fold*foldsize:(fold+1)*foldsize,:,:,:]
    test_mask=mask[fold*foldsize:(fold+1)*foldsize,:,:,:]
  else:
    test_image=sample_data[fold*foldsize:,:,:,:]
    test_mask=mask[fold*foldsize:,:,:,:]
  train_data=TensorDataset(train_image[1:,:,:,:], train_mask[1:,:,:,:])
  test_data=TensorDataset(test_image[1:,:,:,:], test_mask[1:,:,:,:])
  return train_data, test_data


def dice_loss(prediction, true, weight):
  overlap=prediction*true
  sum_overlap=torch.sum(overlap,2)
  sum_overlap=torch.sum(sum_overlap,2)
  prediction_shift=prediction-1
  fn=-prediction_shift*true
  fn_sum=torch.sum(fn,2)
  fn_sum=torch.sum(fn_sum,2)
  true_shift=true-1
  fp=-true_shift*prediction
  fp_sum=torch.sum(fp,2)
  fp_sum=torch.sum(fp_sum,2)
  dice=sum_overlap/(sum_overlap+weight*fp_sum+(1-weight)*fn_sum)
  dice=torch.sum(dice)/dice.shape[0]
  return 1-dice


def model_train(model, train_loader, test_loader, para, fold):
  weight=para['dice_weight']
  optim =torch.optim.Adam(model.parameters(),lr=para['learning_rate'])
  criterion=torch.nn.BCELoss()
  model_save_name='Unet_single_cell_'+str(para['unet_init_kernel'])+'features_bceloss+dice_'+str(weight)+'_fold_'+str(fold)+'.pt'
  path=para['save_path']+'/'+model_save_name
  loss_val=0
  if para['resume']==fold:
     checkpoint=torch.load(path)
     epoch_con = checkpoint['epoch']
     loss_val_store = checkpoint['lowest_loss']
     model.load_state_dict(checkpoint['model_state_dict'])
     optim.load_state_dict(checkpoint['optimizer_state_dict'])
     loss_list=checkpoint['lost_list']
  else:
     loss_list=[]
     epoch_con=0
     loss_val_store=2
  device=para['device']
  print(device)
  model=model.to(device)
  for epochs in range(epoch_con,para['num_epochs']):
    model.train()
    for i, (X,y) in enumerate(train_loader):
      X=X.to(device)
      y=y.to(device)
      prediction=model(X)
      loss=criterion(prediction,y)+dice_loss(prediction,y,weight)
      optim.zero_grad()
      loss.backward()
      optim.step()

    model.eval()
   
    for i ,(X,y) in enumerate(test_loader):
      X=X.to(device)
      y=y.to(device)
      prediction=model(X)
      loss_val=(loss_val*i+criterion(prediction,y).item()+dice_loss(prediction ,y,weight).item())/(i+1)
    
    if loss_val_store > loss_val:
       loss_val_store=loss_val
       model_store=model
    
    loss_list.append([loss.item(),loss_val]) 
    torch.save({'epoch': epochs,'model_state_dict': model.state_dict(),'optimizer_state_dict': optim.state_dict(),'best_model':model_store.state_dict(),'lowest_loss': loss_val_store, 'loss_list':loss_list}, path)
    
    print ('Epoch [{}/{}], training error: {:.4f}, validation Loss: {:.4f}'.format(epochs+1, para['num_epochs'], loss, loss_val))    
  return


def cross_val(kf,sample_data,mask_data,model,para):
  for i in range(kf):
    if para['resume']>i:
      continue   
    train_data, test_data= k_cross_data_split(sample_data, mask_data, para['batch_size'],i,kf)
    train_loader=DataLoader(dataset=train_data, batch_size=para['batch_size'], shuffle=True,drop_last=True)
    test_loader=DataLoader(dataset=test_data, batch_size=para['batch_size'], shuffle=False,drop_last=True)
    print('fold:',i)
    model_train(model,train_loader,test_loader,para,i)
  return
