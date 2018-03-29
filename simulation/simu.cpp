#include <fstream>
#include <iomanip>
#include <limits>
#include "epot_bicgstabsolver.hpp"
#include "meshvectorfield.hpp"
#include "dxf_solid.hpp"
#include "stl_solid.hpp"
#include "stlfile.hpp"
#include "mydxffile.hpp"
#include "gtkplotter.hpp"
#include "geomplotter.hpp"
#include "geometry.hpp"
#include "func_solid.hpp"
#include "epot_efield.hpp"
#include "error.hpp"
#include "ibsimu.hpp"
#include "trajectorydiagnostics.hpp"
#include "particledatabase.hpp"
#include "particlediagplotter.hpp"
#include <readascii.hpp>
#include <math.h>
using namespace std;



//define the variables we need for the geometry. The 5 first einzels are in the straight line and the upper einzels are in the bended section.
//All lengths are in meter, and all voltages are V. 
const double einzel1radius = 0.065;
const double einzel2radius = 0.080;
const double einzel3radius = 0.065;
const double einzel4radius = 0.080;
const double einzel5radius = 0.065;
const double einzel1length = 0.030;
const double einzel2length = 0.150;
const double einzel3length = 0.075;
const double einzel4length = 0.110;
const double einzel5length = 0.040;

const double upperEinzelRadius=0.070;
const double upperEinzelLengthSmall=0.04;
const double upperEinzelLengthLong=0.06;

const double thicknessOfEinzellenses=0.005;
const double distanceBetweenLenzes=0.01;
const double distanceToBendedElectrode=0.0005;
const double distanceToStraightElectrode=0.042;

const double lengthOfStraightLine=1.70;
const double airgap=0.065;
const double xdimensions=1.0;
const double ydimensions=0.3;
const double beam_curve = 40.0; // in degrees
const double GraceRadius=0.1;
const double GraceThickness=0.02;
//const double GraceThickness=0.005;
const double thicknessOfElectrodes=0.005;

//here we set the voltages  of  the einzel lenses and the bending electrodes.  The voltage for the lower einzel is the same for both the rings because they are connected together in the GRACE apparatus. The voltages are initially set to zero, the values actually used are set as inputparameters.  
double lowerEinzel=0.0;
double upperEinzel=0.0;
double HVelectrode1 = 0.0;
double HVelectrode2 = 0.0;

//Here all the beamline elements are defined.  They are defined  as  boolean function that returns true or false. If the x,y,z position given to the function is inside the element it returns true, if not it returns false 

// Here the straight line is defined, with a hole for the bended line  to be placed.   
// bool vacuum1( double x, double y, double z){
//   double x0 = 0.0;
//   double theta=beam_curve*M_PI/180.0;
//   double z0=0.5+0.1/cos(beam_curve*M_PI/180)-0.1/tan(beam_curve*M_PI/180)+0.02/tan(beam_curve*M_PI/180);
//   z=z-z0;
//   double x_rot=cos(theta)*x-sin(theta)*(z);
//   return ( ( x*x + y*y <= (GraceRadius+GraceThickness)*(GraceRadius+GraceThickness) &&
//    	     x*x + y*y >= GraceRadius*GraceRadius) && !(x_rot*x_rot + y*y <= (GraceRadius+GraceThickness)*(GraceRadius+GraceThickness) && x>=0));  
// }

// //Here the bended  line is defined
// bool vacuum2( double x, double y, double z){
//   double  theta=beam_curve*M_PI/180.0;
//   double z0=0.5+0.1/cos(beam_curve*M_PI/180)-0.1/tan(beam_curve*M_PI/180)+0.02/tan(beam_curve*M_PI/180);
//   z=z-z0;
//   double x_rot=cos(theta)*x-sin(theta)*(z);
//   return ( x_rot*x_rot + y*y <= (GraceRadius+GraceThickness)*(GraceRadius+GraceThickness)&&
// 	   x_rot*x_rot + y*y >= (GraceRadius*GraceRadius)&&!(x*x+y*y<GraceRadius*GraceRadius)&&x>-0.1);//&&z>0.0);//&&!(z<3*GraceRadius&&x<GraceRadius));// && !(x<0.0&&z<2.7*GraceRadius));
// }


bool vacuum1( double x, double y, double z){
  double x0 = 0.0;
  double theta=beam_curve*M_PI/180.0;
  double z0=0.5-GraceRadius/tan(theta)+GraceRadius/sin(theta);//+0.5*GraceThickness;//-0.1/sin(beam_curve*M_PI/180);//-0.1/tan(beam_curve*M_PI/180)+0.02/tan(beam_curve*M_PI/180);
  z=z-z0;
  double x_rot=cos(theta)*x-sin(theta)*(z);
  return ( ( x*x + y*y <= (GraceRadius+GraceThickness)*(GraceRadius+GraceThickness) &&
   	     x*x + y*y >= GraceRadius*GraceRadius) && !(x_rot*x_rot + y*y <= (GraceRadius+GraceThickness)*(GraceRadius+GraceThickness) && x>=0));  
}

//Here the bended  line is defined
bool vacuum2( double x, double y, double z){
  double  theta=beam_curve*M_PI/180.0;
  double z0=0.5-GraceRadius/tan(theta)+GraceRadius/sin(theta);// 0.1/sin(beam_curve*M_PI/180);//-0.1/tan(beam_curve*M_PI/180)+0.02/tan(beam_curve*M_PI/180);
  z=z-z0;
  double x_rot=cos(theta)*x-sin(theta)*(z);
  return ( x_rot*x_rot + y*y <= (GraceRadius+GraceThickness)*(GraceRadius+GraceThickness)&&
	   x_rot*x_rot + y*y >= (GraceRadius*GraceRadius)&&!(x*x+y*y<GraceRadius*GraceRadius)&&x>-0.1);//&&z>0.0);//&&!(z<3*GraceRadius&&x<GraceRadius));// && !(x<0.0&&z<2.7*GraceRadius));
}





//This is the bended  electrode
bool hvelectrode1( double x, double y, double z){  
  double  depthOfElectrode=0.05;
  double r_c=0.0845;
  double x0 =r_c+0.06;
  double lengthOfSmallElectrode=0.1;
  double z0=0.1;
  return( 
	 (x-x0)*(x-x0)+(z-z0)*(z-z0) >= r_c*r_c &&
	 (x-x0)*(x-x0)+(z-z0)*(z-z0) <= (r_c+thicknessOfElectrodes)*(r_c+thicknessOfElectrodes)&& z-z0>0 && x<0.08 && x>0.055 && y<depthOfElectrode*0.5 &&y>-depthOfElectrode*0.5) or ((z>0.0)&&(z<lengthOfSmallElectrode)&&( x>0.055) &&( x<(0.055+thicknessOfElectrodes))&&y<depthOfElectrode*0.5&&y>-depthOfElectrode*0.5);
																				  ;
	  }

//This is the straight electrode
bool hvelectrode2( double x, double y, double z){  
  double lengthOfElectrode=0.2;
  double depthOfElectrode=0.12;
  double hightOfElectrode=-0.05;
  return( (z>0.0)&&(z<lengthOfElectrode)&&( x>hightOfElectrode) &&( x<(hightOfElectrode+thicknessOfElectrodes))&&y<depthOfElectrode*0.5&&y>-depthOfElectrode*0.5);
}


//Here are all the 5 einzel lenses in the straight part of the line 
bool einzel1( double x, double y, double z){  
  return (  x*x + y*y <= (einzel1radius+thicknessOfEinzellenses)*(einzel1radius+thicknessOfEinzellenses) &&
	    x*x + y*y >= (einzel1radius)*(einzel1radius) &&
	    z >=0.0 && z<=einzel1length);		
}

bool einzel2( double x, double y, double z){  
  return (  x*x + y*y <= (einzel2radius+thicknessOfEinzellenses)*(einzel2radius+thicknessOfEinzellenses) &&
	    x*x + y*y >= (einzel2radius)*(einzel2radius) &&
	    z >=0.0 && z<=einzel2length);		
}

bool einzel3( double x, double y, double z){  
  return (  x*x + y*y <= (einzel3radius+thicknessOfElectrodes)*(einzel3radius+thicknessOfEinzellenses) &&
	    x*x + y*y >= (einzel3radius)*(einzel3radius) &&
	    z >=0.0 && z<=einzel3length);		
}

bool einzel4( double x, double y, double z){  
  return (  x*x + y*y <= (einzel4radius+thicknessOfEinzellenses)*(einzel4radius+thicknessOfEinzellenses) &&
	    x*x + y*y >= (einzel4radius)*(einzel4radius) &&
	    z >=0.0 && z<=einzel4length);		
}

bool einzel5( double x, double y, double z){  
  return (  x*x + y*y <= (einzel5radius+thicknessOfEinzellenses)*(einzel5radius+thicknessOfEinzellenses) &&
	    x*x + y*y >= (einzel5radius)*(einzel5radius) &&
	    z >=0.0 && z<=einzel5length);		
}


//The upper line consist of three rings, but two of  them are simular therefore only two needs to be defined. 
bool upperEinzelSmall( double x, double y, double z){  
  return (  x*x + y*y <= (upperEinzelRadius+thicknessOfEinzellenses)*(upperEinzelRadius+thicknessOfEinzellenses) &&
	    x*x + y*y >= (upperEinzelRadius)*(upperEinzelRadius) &&
	    z >=0.0 && z<=upperEinzelLengthSmall);		
}

bool upperEinzelLong( double x, double y, double z){  
  return (  x*x + y*y <= (upperEinzelRadius+thicknessOfEinzellenses)*(upperEinzelRadius+thicknessOfEinzellenses) &&
	    x*x + y*y >= (upperEinzelRadius)*(upperEinzelRadius) &&
	    z >=0.0 && z<=upperEinzelLengthLong);		
}


//this element  is an endplate covering the  whole tube where  the  detector  is mounted.  
bool detector( double x, double y, double z){
  return (x*x+y*y <= (GraceRadius)*(GraceRadius)&&z<0.015&&z>-0.015);
}

void simu( int argc, char **argv )
{
  //the voltages  of the  electrodes  and  einzel are set with input parameters
  HVelectrode1=atof(argv[1]);
  HVelectrode2=-atof(argv[2]);
  lowerEinzel=-atof(argv[3]);
  upperEinzel=-atof(argv[4]);
  // sets up size of volume for simulation and mesh size
  double h = 5.0e-3; // mesh size in m
  //double h = atof(argv[8])*1e-3; // mesh size in cm
  double sizereq[3] = { xdimensions,// x-dimension
			ydimensions,// y-dimension
			lengthOfStraightLine+airgap+0.2};// z-dimension
  Int3D meshsize( (int)floor(sizereq[0]/h)+1,
		  (int)floor(sizereq[1]/h)+1,
		  (int)floor(sizereq[2]/h)+1 );
  Vec3D origo( -0.15, -0.15, -0.25); // sets the start corner
  Geometry geom( MODE_3D, meshsize, origo, h );


  double offset=0.0;
  // creates, labels, and adds solids to geometry
  //here the geometry elements are created from the boolean functions,  and translated and rotated to their right position
  Solid *ez1 = new FuncSolid( einzel1);
  ez1->translate(Vec3D(0.0,0.0,offset));
  geom.set_solid( 7, ez1);
  
  Solid *ez2 = new FuncSolid( einzel2);
  ez2->translate(Vec3D(0.0 ,0.0 ,distanceBetweenLenzes+einzel1length+offset));
  geom.set_solid( 8, ez2);

  Solid *ez3 = new FuncSolid( einzel3);
  ez3->translate(Vec3D(0.0 ,0.0 ,2*distanceBetweenLenzes+einzel1length+einzel2length+offset));
  geom.set_solid( 9, ez3);

  Solid *ez4 = new FuncSolid( einzel4);
  ez4->translate(Vec3D(0.0 ,0.0 ,3*distanceBetweenLenzes+einzel1length+einzel2length+einzel3length+offset));
  geom.set_solid( 10, ez4);

  Solid *ez5 = new FuncSolid( einzel5);
  ez5->translate(Vec3D(0.0 ,0.0 , 4*distanceBetweenLenzes+einzel1length+einzel2length+einzel3length+einzel4length+offset));
  geom.set_solid( 11, ez5);

  Solid *hv1 = new FuncSolid( hvelectrode1);
  hv1->translate(Vec3D(0.0 ,0.0 , 4*distanceBetweenLenzes+einzel1length+einzel2length+einzel3length+einzel4length+einzel5length+distanceToBendedElectrode));
  geom.set_solid( 12, hv1);

  Solid *hv2 = new FuncSolid( hvelectrode2);
  hv2->translate(Vec3D(0.0 ,0.0 , 4*distanceBetweenLenzes+einzel1length+einzel2length+einzel3length+einzel4length+einzel5length+distanceToStraightElectrode));
  geom.set_solid( 13, hv2);

  Solid *det = new FuncSolid( detector);
  double d=0.5+GraceRadius/sin(M_PI*beam_curve/180.0);
  //double z_translateion=d+0.85*cos(M_PI*beam_curve/180.0);
  //double x_translateion=GraceRadius+0.85*sin(M_PI*beam_curve/180);
  double z_translateion=d+0.75*cos(M_PI*beam_curve/180.0);
  double x_translateion=GraceRadius+0.75*sin(M_PI*beam_curve/180);
  det->rotate_y(beam_curve*M_PI/180);
  det->translate(Vec3D(x_translateion,0,z_translateion));
  geom.set_solid( 14, det);

  

  Solid *vac1 = new FuncSolid( vacuum1);
  geom.set_solid( 15, vac1);

  Solid *vac2 = new FuncSolid( vacuum2);
  geom.set_solid( 16, vac2);
  
  Solid *smallEinzel=new FuncSolid(upperEinzelSmall);
  d=0.5+GraceRadius/sin(M_PI*beam_curve/180.0);
  double startFirstEinzel=0;
  double up=startFirstEinzel/cos(beam_curve*M_PI/180.0)+offset;
  smallEinzel->rotate_y(beam_curve*M_PI/180);
  z_translateion=d+up;
  x_translateion=GraceRadius+up/tan((90.0-beam_curve)*M_PI/180.0);
  smallEinzel->translate(Vec3D(x_translateion,0,z_translateion));
  geom.set_solid(17,smallEinzel);

  Solid *longEinzel1=new FuncSolid(upperEinzelLong);
  d=0.5+GraceRadius/sin(M_PI*beam_curve/180.0);
  up=(startFirstEinzel+upperEinzelLengthSmall+distanceBetweenLenzes)*cos(beam_curve*M_PI/180)+offset;
  longEinzel1->rotate_y(beam_curve*M_PI/180);
  z_translateion=d+up;
  x_translateion=GraceRadius+up/tan((90.0-beam_curve)*M_PI/180.0);
  longEinzel1->translate(Vec3D(x_translateion,0,z_translateion));
  geom.set_solid(18,longEinzel1);

  Solid *longEinzel2=new FuncSolid(upperEinzelLong);
  d=0.5+GraceRadius/sin(M_PI*beam_curve/180.0);
  up=(startFirstEinzel+upperEinzelLengthSmall+2*distanceBetweenLenzes+upperEinzelLengthLong)*cos(beam_curve*M_PI/180)+offset;
  longEinzel2->rotate_y(beam_curve*M_PI/180);
  z_translateion=d+up;
  x_translateion=GraceRadius+up/tan((90.0-beam_curve)*M_PI/180.0);
  longEinzel2->translate(Vec3D(x_translateion,0,z_translateion));
  geom.set_solid(19,longEinzel2);

  Solid *startPlate = new FuncSolid( detector);
  startPlate->translate(Vec3D(0.0,0.0,-0.026));
  geom.set_solid( 20, startPlate);


  cout<<"her er det"<<endl;
  // the first 6 are the boundaries of the volume of simulation
  geom.set_boundary(  1,  Bound(BOUND_NEUMANN,     0.0) );
  geom.set_boundary(  2,  Bound(BOUND_NEUMANN,     0.0) );
  geom.set_boundary(  3,  Bound(BOUND_NEUMANN,     0.0) );
  geom.set_boundary(  4,  Bound(BOUND_NEUMANN,     0.0) );
  geom.set_boundary(  5,  Bound(BOUND_DIRICHLET,   0.0) );
  geom.set_boundary(  6,  Bound(BOUND_DIRICHLET,   0.0) );
  geom.set_boundary(  7,  Bound(BOUND_DIRICHLET,   0.0) );
  geom.set_boundary(  8,  Bound(BOUND_DIRICHLET,   lowerEinzel) );
  geom.set_boundary(  9,  Bound(BOUND_DIRICHLET,   0.0) );
  geom.set_boundary(  10,  Bound(BOUND_DIRICHLET,  lowerEinzel) );
  geom.set_boundary(  11,  Bound(BOUND_DIRICHLET,  0.0) );
  geom.set_boundary( 12,  Bound(BOUND_DIRICHLET,   HVelectrode1) ); 
  geom.set_boundary(  13,  Bound(BOUND_DIRICHLET,  HVelectrode2) );
  geom.set_boundary(  14,  Bound(BOUND_DIRICHLET,  0.0) );
  geom.set_boundary(  15,  Bound(BOUND_DIRICHLET,  0.0) );
  geom.set_boundary(  16,  Bound(BOUND_DIRICHLET,  0.0) );
  geom.set_boundary(  17,  Bound(BOUND_DIRICHLET,  0.0) );
  geom.set_boundary(  18,  Bound(BOUND_DIRICHLET,  upperEinzel) );
  geom.set_boundary(  19,  Bound(BOUND_DIRICHLET,  0.0) );
  geom.set_boundary(  20,  Bound(BOUND_DIRICHLET,  0.0) );
  geom.build_mesh();
  geom.build_surface();

  cout<<"ferdig"<<endl;
  
  //solve for potential in the given geometry
  EpotField epot( geom );
  MeshScalarField scharge( geom );
  MeshScalarField scharge_ave( geom );
  // Define magnetic field, by default it is zero.  We use the default
  MeshVectorField bfield;
  EpotEfield efield( epot );
  field_extrpl_e efldextrpl[6] = { FIELD_EXTRAPOLATE, FIELD_EXTRAPOLATE,
				   FIELD_EXTRAPOLATE, FIELD_EXTRAPOLATE,
				   FIELD_EXTRAPOLATE, FIELD_EXTRAPOLATE };
  efield.set_extrapolation( efldextrpl );
  EpotBiCGSTABSolver solver( geom );
  ParticleDataBase3D pdb( geom );
  pdb.set_max_steps( 10000 );

  //here we set if the particles  are reflected off the wall.  By setting  these to false  the particle is killed when they hit solid material
  bool pmirror[7] = { false, false, false, false, false, false, false };
  pdb.set_mirror( pmirror );
  
  // in the following section we make the  particle database and find the trajectories of the particles in the geometry. To take into account space charge this procedure should be repeated until  it converges, but in the GRACE beamline the flux is so low that it is not necassary.
  
  //define the solver. 
  solver.solve( epot, scharge_ave );
  efield.recalculate();
  pdb.clear();


  //The inputfile giving  the energy,position and momentum  direction of the particles  are read  in.  
  ReadAscii din(argv[5], 8 );
  cout<< "Reading this "<<argv[5]<<endl;
  cout << "Reading " << din.rows() << " particles\n";
  // Loop  over all  the particles. We also make a vector of strings with the inital parameters so they can be stored for later analysis
  std::vector<string> initialParameters;
  int counter=0;
  for( size_t l = 0; l < din.rows();l++ ) {
    counter+=1;
    //The original line in the inputfile. 
    string initialLine=to_string(din[0][l])+"  "+to_string(din[1][l])+"  "+to_string(din[2][l])+"  "+to_string(din[3][l])+"  "+to_string(din[4][l])+"  "+to_string(din[5][l]) +"  "+to_string(din[6][l])+"  ";
    
    double I  = 1.0;//the current (not used since  we don't care about space charge) 
    double m  = 1.0;//mass of the particle in terms of u
    double q = -1.0;//Charge of the particle in terms of elementary charge
    double t  = 0.0;//start time
    double test=(din[1][l]);
    double x  = (din[2][l])*1e-2;//x  start positin (in meter)
    double y  = (din[3][l])*1e-2;//y  start positin (in meter)
    double z  = -1.0*1e-2;//z  start position (in meter)
    double energy = din[0][l];//the energy of the particle (in keV)
    
    //since  we are not interested in particles with lower than 10 keV energy we skip them here to save computation time
     if (energy>13.0){
      continue;
     }
    if (test>3.00){
      cout<<"fant dobbel"<<endl;
      continue;
    }
    // if (counter>10000){
    //   cout<<"counter"<<counter<<endl;
    //   continue;
    // }
   
    //here the  velocity of the particle is  calculated  by using the relativistic  energy 
    double c=299792458.0;
    double m0=938272.0;
    double v_tot_r=sqrt(1-(m0*m0/((m0+din[0][l])*(m0+din[0][l]))))*c;


    //we find  the velocity of the particle in x,y and x direction 
    double vx = v_tot_r*din[5][l];
    double vy = v_tot_r*din[6][l];
    double vz =v_tot_r*din[4][l];

    
    pdb.add_particle( I, q, m, ParticleP3D(t,x,vx,y,vy,z,vz) );
    initialParameters.push_back(initialLine);
    
  }
  
  //We find the trajectories of the particles in GRACE
  pdb.iterate_trajectories( scharge, efield, bfield );

  // save data for plotting
  geom.save( "geom.dat" );
  epot.save( "epot.dat" );
  pdb.save( "pdb.dat" );

  //also want to write to the field to file

  // cout<<"start here"<<endl;
  // double zValueForField=0.5;
  // for (double xValueForField=-0.15;xValueForField<0.15;xValueForField+=0.01){
  //   for (double yValueForField=-0.15;yValueForField<0.15;yValueForField+=0.01){
  //     cout<<xValueForField<<"  "<<yValueForField<<"  "<<zValueForField<<endl;
  //     cout<<"epotential "<<epot.operator()(Vec3D(xValueForField,yValueForField,zValueForField))<<endl;
  //   }
  // }


  
  //define the name of the outputfile
  string outputfile=string(argv[6])+"/D1_"+string(argv[1])+"D2_"+string(argv[2])+"E1_"+string(argv[3])+"E2_"+string(argv[4])+"_scanning"+string(argv[7])+".txt";
  ofstream fileOut(outputfile.c_str());
  string lineNumberOutputfile=outputfile+"lineNumber";
  
  //here we iterate over the particle database to write all informationto file.


  double maxLength=0;
  for( size_t k = 0; k < pdb.size(); k++ ) {
    Particle3D &pp = pdb.particle( k );
      //write the final  locatiion and energy to files
    fileOut<< pp.location()<<"  "<<6.24e15*pp.m()*(pp(2)*pp(2)+pp(4)*pp(4)+pp(6)*pp(6))/2.0<<"  "<<pp(0)*1000000000.0<<"  "<<pdb.traj_length(k);
      //reset the trajectory to find the initial position, momentum directions and energy of the particle

    if(pdb.traj_length(k)>maxLength){
      maxLength=pdb.traj_length(k);
    }
    //cout<<"length "<<maxLength<<endl;
    //cout<<pp.traj(0)<<endl;
    //cout<<pp(0)*1000000000<<endl;
    pp.reset_trajectory();
    //cout<<pp(0)*1000000000<<endl;
    //print that information to file
    fileOut <<"initial "<<initialParameters[k]<< "\n";
    //fileOut <<"initial "<<pp.location()<<"  ";
    //fileOut <<pp(2)/vtotal<<"   "<<pp(4)/vtotal<<"  "<<pp(6)/vtotal<<"  "<<6.2415096471e15*1.6e-27*(pp(2)*pp(2)+pp(4)*pp(4)+pp(6)*pp(6))/2.0<<"\n";
  }
  fileOut.close();
}

int main( int argc, char **argv )
{

    if( argc != 8) {
	cerr << "Usage: bending1 bending2 einzel1 enizel2 inputfil outputfolder outputname\n";
	exit( 1 );
    }
  
  
  cout<<string(argv[6])+"/D1_"+string(argv[1])+"D2_"+string(argv[2])+"E1_"+string(argv[3])+"E2_"+string(argv[4])+"_scanning"+string(argv[7])+".txt"<<endl;

  try {
    ibsimu.set_message_threshold( MSG_VERBOSE, 1 );
    simu( argc, argv );
  } catch( Error e ) {
    e.print_error_message( ibsimu.message( 0 ) );
    exit( 1 );
  }
  return( 0 );
}
