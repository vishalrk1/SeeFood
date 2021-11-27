import 'dart:io';

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
        model: "assets/mobilenet_v1_1.0_224.tflite",
        labels: "assets/labels.txt",
        numThreads: 1,
        isAsset: true,
        useGpuDelegate: false);
  }
}
