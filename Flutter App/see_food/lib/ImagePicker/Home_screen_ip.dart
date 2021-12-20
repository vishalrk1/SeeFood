import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:see_food/ImagePicker/DataProvider.dart';
import 'package:tflite/tflite.dart';

import 'PickImage.dart';

class HomePageScreen extends StatefulWidget {
  const HomePageScreen({Key? key}) : super(key: key);

  @override
  _HomePageScreenState createState() => _HomePageScreenState();
}

class _HomePageScreenState extends State<HomePageScreen> {

  var recognitions = await Tflite.runModelOnBinary(
    binary: imageToByteListFloat32(image, 224, 127.5, 127.5),// required
    numResults: 6,    // defaults to 5
    threshold: 0.05,  // defaults to 0.1
    asynch: true      // defaults to true
  );

  Uint8List imageToByteListFloat32(Image image, int inputSize, double mean, double std) {
    var convertedBytes = Float32List(1 * inputSize * inputSize * 3);
    var buffer = Float32List.view(convertedBytes.buffer);
    int pixelIndex = 0;
    for (var i = 0; i < inputSize; i++) {
      for (var j = 0; j < inputSize; j++) {
        var pixel = image.getPixel(j, i);
        buffer[pixelIndex++] = (img.getRed(pixel) - mean) / std;
        buffer[pixelIndex++] = (img.getGreen(pixel) - mean) / std;
        buffer[pixelIndex++] = (img.getBlue(pixel) - mean) / std;
      }
    }
    return convertedBytes.buffer.asUint8List();
  }

  Uint8List imageToByteListUint8(img.Image image, int inputSize) {
    var convertedBytes = Uint8List(1 * inputSize * inputSize * 3);
    var buffer = Uint8List.view(convertedBytes.buffer);
    int pixelIndex = 0;
    for (var i = 0; i < inputSize; i++) {
      for (var j = 0; j < inputSize; j++) {
        var pixel = image.getPixel(j, i);
        buffer[pixelIndex++] = img.getRed(pixel);
        buffer[pixelIndex++] = img.getGreen(pixel);
        buffer[pixelIndex++] = img.getBlue(pixel);
      }
    }
    return convertedBytes.buffer.asUint8List();
  }

  @override
  Widget build(BuildContext context) {
    final dataprovider = Provider.of<DataProvide>(context);
    return Scaffold(
      appBar: AppBar(
        title: Text('Test App'),
      ),
      body: Center(
          child: Column(
        children: [
          SizedBox(
            height: 50,
          ),
          IconButton(
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => PickIimage(),
              );
            },
            icon: Icon(
              Icons.camera,
            ),
          ),
          SizedBox(
            height: 20,
          ),
          dataprovider.pickedImage != null
              ? Image.file(dataprovider.pickedImage!)
              : Container()
        ],
      )),
    );
  }
}
