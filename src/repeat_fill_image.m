clear
clc

ground_truth = dir('C:\Users\tonyg\Desktop\project\fibroblast\merge');
mask=dir('C:\Users\tonyg\Desktop\project\fibroblast\mask');
path1='C:\Users\tonyg\Desktop\project\fibroblast\repeat';
path2='C:\Users\tonyg\Desktop\project\cardiomyocyte\repeat clean merge50%\groundtruth';
        
copyinfo=struct2table(ground_truth);
NF = length(mask);
NF1 =length(ground_truth);

if NF==NF
    images_truth = cell(NF,1);
    images_mask=cell(NF,1);
    images_final_mask=images_truth;
    for k = 13 : NF
        images_truth{k} = imread(fullfile('C:\Users\tonyg\Desktop\project\fibroblast\merge', ground_truth(k).name));
        images_mask{k}=imread(fullfile('C:\Users\tonyg\Desktop\project\fibroblast\mask',mask(k).name));
             
        if(length(size(images_mask{k})))>2
            images_mask{k}=images_mask{k}(:,:,1);
        end
        dim=size(images_truth{k});
        if dim(3)>3
            images_truth{k}=images_truth{k}(:,:,1:3);
        end
        images_mask{k}=im2bw(images_mask{k});
        image_final=[];
        mask_final=[];
        row_sum=sum(images_mask{k}(:,:,1),2);
        row_dim=length(row_sum);
        row_start_index=[];
        row_end_index=[];
        flag=0;
        for i=1:row_dim
            if row_sum(i)~=0 && isempty(row_start_index)
                row_start_index=i;
                flag=flag+1;
            end
            if row_sum(row_dim+1-i)~=0 && isempty(row_end_index)
                row_end_index=513-i;
                flag=flag+1;
            end
            if flag>1
                continue
            end
        end
        column_sum=sum(images_mask{k},1);
        column_dim=length(column_sum);
        column_start_index=[];
        column_end_index=[];
        flag=0;
        for j=1:column_dim
            if column_sum(j)~=0 && isempty(column_start_index)
                column_start_index=j;
            end
            if column_sum(column_dim+1-j)~=0&&isempty(column_end_index)
                column_end_index=1025-j;
            end
            if flag>1
                continue
            end
        end
        image_pri=images_truth{k}(row_start_index:row_end_index, column_start_index:column_end_index,:);
        mask_pri=images_mask{k}(row_start_index:row_end_index, column_start_index:column_end_index);
        dim1=size(image_pri);
        i=dim1(1);
        j=dim1(2);
        while i<=512
            image_final=[image_final;image_pri];
            mask_final=[mask_final;mask_pri];
            i=i+dim1(1);
            image_pri=flip(image_pri);
        end
        image_final=[image_final;image_pri(1:rem(512,dim1(1)),:,:)];
        mask_final=[mask_final;mask_pri(1:rem(512,dim1(1)),:)];
        image_pri=flip(image_final,2);
        mask_pri=mask_final;
        while j+dim1(2)<=1024
            image_final=[image_final,image_pri];
            mask_final=[mask_final,mask_pri];
            j=j+dim1(2);
            image_pri=flip(image_pri,2);
        end
        image_final=[image_final,image_pri(:,1:rem(1024,dim1(2)),:)];       
        mask_final=[mask_final, mask_pri(:,1:rem(1024,dim1(2)))];
        imshow(image_final);
        saveas(gcf, fullfile(path1, copyinfo.name{k}), 'tiffn');
        
        %imshow(mask_final);
        %saveas(gcf, fullfile(path2, copyinfo.name{k}), 'tiffn');
    end
end