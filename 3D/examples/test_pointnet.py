import open3d as o3d
import argparse
import os
import sys
import logging
import numpy
import numpy as np
import torch
import torch.utils.data
import torchvision
from torch.utils.data import DataLoader
from tensorboardX import SummaryWriter
from tqdm import tqdm

# Only if the files are in example folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR[-8:] == 'examples':
	sys.path.append(os.path.join(BASE_DIR, os.pardir))
	os.chdir(os.path.join(BASE_DIR, os.pardir))
	
from models import PointNet
from models import Classifier
from data_utils import ClassificationData, NIAData # , ModelNet40Data

from sklearn.metrics import confusion_matrix
from openpyxl import Workbook

def display_open3d(template):
	template_ = o3d.geometry.PointCloud()
	template_.points = o3d.utility.Vector3dVector(template)
	# template_.paint_uniform_color([1, 0, 0])
	o3d.visualization.draw_geometries([template_])

def test_one_epoch(device, model, test_loader, testset):
	write_wb = Workbook()
	sheet = write_wb.active
	sheet.append(["Class_ID", "TP", "TN", "FP", "FN", "Accuracy"])
	model.eval()
	test_loss = 0.0
	pred  = 0.0
	count = 0
	label = []
	acc = [0 for i in range(4)]
	ca_sum = [[0,0],[0,0]]
	for i, data in enumerate(tqdm(test_loader)):
		
		points, target = data['data'], data['label']
		target = target #[:,0]

		points = points.to(device)
		target = target.to(device)

		output = model(points)
		loss_val = torch.nn.functional.nll_loss(
			torch.nn.functional.log_softmax(output, dim=1), target, size_average=False)

		test_loss += loss_val.item()
		count += output.size(0)

		_, pred1 = output.max(dim=1)
		ag = (pred1 == target)
		am = ag.sum()
		pred += am.item()

	test_loss = float(test_loss)/count
	accuracy = float(pred)/count
	print('Total Accuracy: %f' % accuracy)
	write_wb.save('accuracy.xlsx')
	return test_loss, accuracy

def test(args, model, test_loader, testset):
	test_loss, test_accuracy = test_one_epoch(args.device, model, test_loader, testset)

def options():
	parser = argparse.ArgumentParser(description='Point Cloud Registration')
	parser.add_argument('--dataset_path', type=str, default='new_NIA',
						metavar='PATH', help='path to the input dataset') # like '/path/to/ModelNet40'
	parser.add_argument('--eval', type=bool, default=False, help='Train or Evaluate the network.')

	# settings for input data
	parser.add_argument('--dataset_type', default='modelnet', choices=['modelnet', 'shapenet2'],
						metavar='DATASET', help='dataset type (default: modelnet)')
	parser.add_argument('--num_points', default=1024, type=int,
						metavar='N', help='points in point-cloud (default: 1024)')

	# settings for PointNet
	parser.add_argument('--pointnet', default='tune', type=str, choices=['fixed', 'tune'],
						help='train pointnet (default: tune)')
	parser.add_argument('-j', '--workers', default=4, type=int,
						metavar='N', help='number of data loading workers (default: 4)')
	parser.add_argument('-b', '--batch_size', default=1, type=int,
						metavar='N', help='mini-batch size (default: 32)')
	parser.add_argument('--emb_dims', default=1024, type=int,
						metavar='K', help='dim. of the feature vector (default: 1024)')
	parser.add_argument('--symfn', default='max', choices=['max', 'avg'],
						help='symmetric function (default: max)')

	# settings for on training
	parser.add_argument('--pretrained', default='checkpoints/NIA(공예,조각,건축,악기)_final/models/model.t7', type=str,
						metavar='PATH', help='path to pretrained model file (default: null (no-use))')
	parser.add_argument('--device', default='cuda:1', type=str,
						metavar='DEVICE', help='use CUDA if available')
	parser.add_argument('--seed', type=int, default=1234)

	args = parser.parse_args()
	return args

def main():
	args = options()
	# args.dataset_path = os.path.join(os.getcwd(), os.pardir, os.pardir, 'ModelNet40', 'ModelNet40')
	
	torch.backends.cudnn.deterministic = True
	torch.manual_seed(args.seed)
	torch.cuda.manual_seed_all(args.seed)
	np.random.seed(args.seed)

	testset = NIAData(loadbool=True, train=False, load=True)
	test_loader = DataLoader(testset, batch_size=args.batch_size, shuffle=False, drop_last=False, num_workers=args.workers)

	if not torch.cuda.is_available():
		args.device = 'cpu'
	args.device = torch.device(args.device)

	# Create PointNet Model.
	ptnet = PointNet(emb_dims=args.emb_dims, use_bn=True)
	model = Classifier(feature_model=ptnet)

	if args.pretrained:
		assert os.path.isfile(args.pretrained)
		model.load_state_dict(torch.load(args.pretrained, map_location='cpu'))
	model.to(args.device)

	test(args, model, test_loader, testset)

if __name__ == '__main__':
	main()