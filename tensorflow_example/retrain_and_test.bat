del output_graph.pb
del output_labels.txt
python retrain.py --image_dir ../data --output_labels ./output_labels.txt --output_graph ./output_graph.pb --bottleneck_dir ./bottleneck
python label_image.py --image=./shoe_test_images/nike_air_max_test.jpg --labels=output_labels.txt --graph=output_graph.pb --input_layer=Placeholder --output_layer=final_result
