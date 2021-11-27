import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

import 'DataProvider.dart';

class PickIimage extends StatefulWidget {
  PickIimage({Key? key}) : super(key: key);

  @override
  _PickIimageState createState() => _PickIimageState();
}

class _PickIimageState extends State<PickIimage> {
  @override
  Widget build(BuildContext context) {
    final getImg = Provider.of<DataProvide>(context, listen: false);
    return AlertDialog(
      title: Text(
        "Options",
        style: Theme.of(context)
            .textTheme
            .subtitle1!
            .copyWith(fontWeight: FontWeight.bold),
      ),
      content: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ignore: deprecated_member_use
            FlatButton.icon(
              onPressed: () {
                getImg.pickImage(ImageSource.gallery);
                Navigator.pop(context, true);
              },
              label: Text(
                "Choose From Gallery",
                style: Theme.of(context).textTheme.subtitle2,
              ),
              icon: Icon(
                Icons.folder,
                color: Colors.amber[400],
              ),
            ),
            // ignore: deprecated_member_use
            FlatButton.icon(
              onPressed: () {
                getImg.pickImage(ImageSource.camera);
                Navigator.pop(context, true);
              },
              label: Text(
                "Take Image",
                style: Theme.of(context).textTheme.subtitle2,
              ),
              icon: Icon(
                Icons.camera,
                color: Colors.amber[400],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
