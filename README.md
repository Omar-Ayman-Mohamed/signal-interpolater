# signal-interpolater
Desktop application that illustrates curve fitting efficiency and generates an error map to visualize error 

We desgined a GUI using tkinter python to illustrate the efficiency of polynomial interpolation and visualizing the error using error maps\
The application supports the following features:\
1.Import a signal from an excel sheet (CSV)\
2.Display the signal as a plot\
3.Choose fitting polynomial order\
4.Divide signal into chunks to get a better fitting\
5.Control overlap percentage to check the error due to overlapping chunks\
6.Show polynomial coefficients in latex format for choosed chunk\
7.Show error due to curve fitting\
8.Clip fitted data and extrapolate it to get the whole signal\
9.Generate an error map by choosing two axis parameters and one constant parameter from\(InterpolationOrder,NumberOfChunks, and OverlappingPercentage)\
10.The color map can easily show the best parameters values that result in least error

The following video shows the main application functionalities:



https://user-images.githubusercontent.com/101192969/157312517-4803c797-37e2-4cad-81f3-57e6be02c660.mp4



