# Automated Built Infrastructure Detection in the Arctic Using Submeter Resolution Satellite Imagery
## Credit
[Convolutional Neural Networks for Automated Built Infrastructure Detection in the Arctic Using Sub-Meter Spatial Resolution Satellite Imagery](https://www.mdpi.com/2072-4292/14/11/2719)

## Dataset

In most remote sensing applications of a CNN, annotated data would need to be produced by drawing features of interest through an on-screen digitizing process.
In our experiment, we were able to obtain such a detaest from two sources: OpenStreetMap and Annotated data for the Utqiagvik study site comprised a geospatial
vector dataset of building footprints (polygon features) and road centerlines (line features), which were digitized by the North Slope Borough (NSB) GIS division.
Additionally, we need to manual edit data because we need to ensure that polygon features corresponding to specific buildings and roads aligned with those structurs
in the aerial imagery, and apply a buffer to road centerlines to convert them to polygons.



Imagery layer

[Alaska Department of Natural Resources](http://dnr.alaska.gov/) 

Annotated layer

[North Slope Borough ArcGIS Portal](https://gis-public.north-slope.org/portal/home/) Needs VPN if your IP dose not  belong to The U.S

[OpenStreetMap](https://www.openstreetmap.org/)



## Results

To see the detailed report, click [my report](https://github.com/Wealhour/Automated-Built-Infrastructure-Detection-in-the-Arctic-Using-Submeter-Resolution-Satellite-Imagery/blob/main/CAMS__Wang_.pdf)


The results of this study indicate that the Unet++ model outperforms DeepLabv3 and PSPNet in terms of semantic segmentation accuracy on the Utqiagvik dataset . Additionally, decreasing the dataset size and improving the class balance can further improve the performance of the model.

<p align="center">
<img width="550" alt="Screenshot 2023-02-13 at 20 16 25" src="https://github.com/Wealhour/CCENproject/assets/50286429/97651262-704f-4135-a047-9257b38e6d7e">
</p>

<p align="center">
<img width="550" alt="Screenshot 2023-02-13 at 20 16 25" src="https://github.com/Wealhour/CCENproject/assets/50286429/925785fa-d88c-48d0-85eb-dc5b2294a364">
</p>




## Declaration
Student project, for educational use only.

















