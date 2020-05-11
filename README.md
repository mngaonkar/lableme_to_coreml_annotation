# Convert LableMe annotation JSON to Core ML

`python3 ./convert_labelme_json_to_coreml.py <image directory>`

Note, image directory should have images and corresponding JSON annotation saved from LabelMe tool. The images are copied to saved_images directory with single annotation file annotations.json.
Images are copied again in saved_images just incase there are mismatch in image files and annotation JSON.
