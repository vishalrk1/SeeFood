import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'package:tflite/tflite.dart';

class DataProvide with ChangeNotifier {
  late File uploadedImage;
  File? pickedImage;
  ImagePicker _picker = ImagePicker();

  void getImage(File img) {
    this.pickedImage = img;
    notifyListeners();
  }

  Future<void> pickImage(ImageSource source) async {
    try {
      final image = await _picker.pickImage(source: source, imageQuality: 70);
      if (image == null) return;
      final imageTemporary = File(image.path);
      // setState(() {
      //   this.pickedImage = imageTemporary;
      // });
      pickedImage = imageTemporary;
      notifyListeners();
    } on PlatformException catch (e) {
      print("failed to pick Image: $e");
    }
  }

  Future loadModel() async {
    Tflite.close();
    String? res = await Tflite.loadModel(
      model: "assets/Models/Seefood_model_V2.tflite",
      labels: "assets/labels.txt",
      numThreads: 1,
      isAsset: true,
      useGpuDelegate: false,
    );
  }

//   var recognitions = await Tflite.runModelOnBinary(
//     binary: imageToByteListFloat32(image, 224, 127.5, 127.5),// required
//     numResults: 6,    // defaults to 5
//     threshold: 0.05,  // defaults to 0.1
//     asynch: true      // defaults to true
//   );

//   Uint8List imageToByteListFloat32(img.Image image, int inputSize, double mean, double std) {
//     var convertedBytes = Float32List(1 * inputSize * inputSize * 3);
//     var buffer = Float32List.view(convertedBytes.buffer);
//     int pixelIndex = 0;
//     for (var i = 0; i < inputSize; i++) {
//       for (var j = 0; j < inputSize; j++) {
//         var pixel = image.getPixel(j, i);
//         buffer[pixelIndex++] = (img.getRed(pixel) - mean) / std;
//         buffer[pixelIndex++] = (img.getGreen(pixel) - mean) / std;
//         buffer[pixelIndex++] = (img.getBlue(pixel) - mean) / std;
//       }
//     }
//   return convertedBytes.buffer.asUint8List();
// }

}
