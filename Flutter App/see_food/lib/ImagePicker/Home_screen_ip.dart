import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:see_food/ImagePicker/DataProvider.dart';

import 'PickImage.dart';

class HomePageScreen extends StatefulWidget {
  const HomePageScreen({Key? key}) : super(key: key);

  @override
  _HomePageScreenState createState() => _HomePageScreenState();
}

class _HomePageScreenState extends State<HomePageScreen> {
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
