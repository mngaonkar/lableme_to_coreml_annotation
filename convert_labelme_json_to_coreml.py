import os
import sys
import json
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

SAVED_IMAGES_DIR = 'saved_images'

def main():
	if len(sys.argv) != 2:
		print("invalid command line arguments")
		sys.exit(1)

	image_dir = sys.argv[1]
	final_annotations = []
	total_images = 0
	
	if not os.path.isdir(os.path.join(image_dir, SAVED_IMAGES_DIR)):
		print('saved_images directory not present, creating it...')
		os.mkdir(os.path.join(image_dir, SAVED_IMAGES_DIR))

	annotation_files = os.listdir(image_dir)
	for file in annotation_files:
		if file.split('.')[-1] == 'json':
			# check if corresponding image file is present
			image_file = '.'.join(file.split('.')[:-1])
			print('processing ', image_file)
			image_annotations = {}

			if os.path.isfile(os.path.join(image_dir, image_file + '.jpg')):
				image_annotations['image'] = image_file + '.jpg'
			elif os.path.isfile(os.path.join(image_dir, image_file + '.jpeg')):
				image_annotations['image'] = image_file + '.jpeg'
			elif os.path.isfile(os.path.join(image_dir, image_file + '.png')):
				image_annotations['image'] = image_file + '.png'
			else:
				print('no file image found for json ', file.split('.')[0])
				continue

			# copy image file to a new folder
			shutil.copyfile(os.path.join(image_dir, image_annotations['image']), 
				os.path.join(image_dir, SAVED_IMAGES_DIR, image_annotations['image']))

			# read JSON file
			payload = json.load(open(os.path.join(image_dir, file), 'r'))
			image_annotations['annotations'] = []
			for item in payload['shapes']:
				# print(item)
				annotation = {}
				annotation['label'] = item['label']
				annotation['coordinates'] = {
					'x': (item['points'][0][0] + item['points'][1][0])/2,
					'y': (item['points'][0][1] + item['points'][1][1])/2,
					'width': item['points'][1][0] - item['points'][0][0],
					'height': item['points'][1][1] - item['points'][0][1],
				}
				if (item['points'][1][0] - item['points'][0][0]) > 0 and \
					(item['points'][1][1] - item['points'][0][1]) > 0:
					image_annotations['annotations'].append(annotation)

			# print(image_annotations)
			final_annotations.append(image_annotations)
			total_images += 1

	print('total images processed = ', total_images)
	fp = open(os.path.join(image_dir, SAVED_IMAGES_DIR, 'annotations.json'), 'w')
	print(final_annotations)
	json_file = json.dumps(final_annotations)
	fp.write(json_file)
	fp.close()

def visualize_image(image_file):
	im = np.array(Image.open(image_file), dtype=np.uint8)
	fig, ax = plt.subplots(1)
	ax.imshow(im)

	annotations = json.load(open('/'.join(image_file.split('/')[:-1]) + "/annotations.json", "r"))
	for item in annotations:
		if item['image'] == image_file.split('/')[-1]:
			annotation = item['annotations']
			print(annotation)
			for location in annotation:
				x = location['coordinates']['x'] - location['coordinates']['width']/2
				y = location['coordinates']['y'] - location['coordinates']['height']/2
				width = location['coordinates']['width']
				height = location['coordinates']['height']

				rect = patches.Rectangle((x,y), width, height, linewidth=3, edgecolor='r', facecolor='none')
				ax.add_patch(rect)
		else:
			continue

	plt.show()

if __name__ == '__main__':
	main()
	# visualize_image("images/saved_images/iStock-874686094b-medium.jpg")
