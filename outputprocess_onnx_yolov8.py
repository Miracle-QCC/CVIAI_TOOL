import cv2
import cv2.dnn
import numpy as np
import torch
import onnxruntime
import sys
import torch
import tqdm
import onnx
from onnx import numpy_helper
#

model = onnx.load("/home/qcj/workcode/yolov8/tools/runs/qat/train2/weights/mqbench_qmodel_deploy_model.onnx")
node_to_split = [model.graph.node[-3], model.graph.node[-2],model.graph.node[-1]]
output1 = model.graph.node[-3]
output2 = model.graph.node[-2]
output3 = model.graph.node[-1]

output1_shape_1 = [1,64,48,80]
output1_tensor_1 = onnx.helper.make_tensor_value_info("8_box",onnx.TensorProto.FLOAT, output1_shape_1)
output1_shape_2 = [1,6,48,80]
output1_tensor_2 = onnx.helper. make_tensor_value_info("8_cls",onnx.TensorProto.FLOAT, output1_shape_2)

split_node1 = onnx.helper.make_node("Split", inputs=["2590"], outputs=["8_box", "8_cls"], axis=1,split=[64,6])


output2_shape_1 = [1,64,24,40]
output2_tensor_1 = onnx.helper.make_tensor_value_info("16_box",onnx.TensorProto.FLOAT, output2_shape_1)
output2_shape_2 = [1,6,24,40]
output2_tensor_2 = onnx.helper. make_tensor_value_info("16_cls",onnx.TensorProto.FLOAT, output2_shape_2)

split_node2 = onnx.helper.make_node("Split", inputs=["2644"], outputs=["16_box", "16_cls"], axis=1,split=[64,6])

output3_shape_1 = [1,64,12,20]
output3_tensor_1 = onnx.helper.make_tensor_value_info("32_box",onnx.TensorProto.FLOAT, output3_shape_1)
output3_shape_2 = [1,6,12,20]
output3_tensor_2 = onnx.helper. make_tensor_value_info("32_cls",onnx.TensorProto.FLOAT, output3_shape_2)

split_node3 = onnx.helper.make_node("Split", inputs=["2698"], outputs=["32_box", "32_cls"], axis=1,split=[64,6])

for i,node in enumerate(model.graph.node):
    if node.output[0] == "2590":
        # output1.output[0] = "split_output"
        model.graph.node.insert(i+1, split_node1)

    elif node.output[0] == "2644":
        # output1.output[0] = "split_output"
        model.graph.node.insert(i + 1, split_node2)

    elif node.output[0] == "2698":
        # output1.output[0] = "split_output"
        model.graph.node.insert(i + 1, split_node3)

# model.graph.output.remove(tensor_to_split1)
model.graph.output.extend([output1_tensor_1, output1_tensor_2, output2_tensor_1, output2_tensor_2,
                           output3_tensor_1, output3_tensor_2])
onnx.save(model,"second_origin_split_yolov8n.onnx")

# input_data = np.zeros((1,3,384,640)).astype(np.float32)
# output_names = ['2590', '2644', '2698']
# sess = onnxruntime.InferenceSession("mqbench_qmodel_deploy_model.onnx")
# outputss = sess.run(None, {'data':input_data})
# outputs = [output1,output2,output3]
# outputs_tensor = [torch.from_numpy(_) for _ in outputs]
# concat_output = torch.cat(outputs_tensor, axis=0)