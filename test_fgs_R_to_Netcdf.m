load fgs_R_DB_two_402.mat
fgs = fgs_R;
clear fgs_R;

% Set NaN values to fill value for NetCDF
fgs.z(isnan(fgs.z)) = -99999;
fgs.zhat(isnan(fgs.zhat)) = -99999;

if ~is_valid_struct(fgs)
    error('    Argument to fgs_R_ToNetcdf must be a valid fem_grid_struct.')
end

f='twm_example.nc';
if exist(f,'file'),delete(f),end


nccreate(f,'x','Dimensions',{'node' size(fgs.x,1)},'Format','netcdf4');
    ncwriteatt(f,'x','long_name','longitude');
    ncwriteatt(f,'x','standard_name','longitude');
    ncwriteatt(f,'x','units','degrees_east');
    ncwriteatt(f,'x','positive','east');

nccreate(f,'y','Dimensions',{'node' size(fgs.y,1)},'Format','netcdf4');
    ncwriteatt(f,'y','long_name','latitude');
    ncwriteatt(f,'y','standard_name','latitude');
    ncwriteatt(f,'y','units','degrees_north');
    ncwriteatt(f,'y','positive','north');

nccreate(f,'maxele','Dimensions',{'node' size(fgs.z,1)},'Format','netcdf4');
    ncwriteatt(f,'maxele','long_name','maxele');
    ncwriteatt(f,'maxele','standard_name','maxele');
    ncwriteatt(f,'maxele','mesh','adcirc_mesh');
    ncwriteatt(f,'maxele','units','m');
    ncwriteatt(f,'maxele','location','node');
    ncwriteatt(f,'maxele','FillValue','-99999');

nccreate(f,'maxele_prediction','Dimensions',{'node' size(fgs.zhat,1)},'Format','netcdf4');
    ncwriteatt(f,'maxele_prediction','long_name','maxele_prediction');
    ncwriteatt(f,'maxele_prediction','standard_name','maxele_prediction');
    ncwriteatt(f,'maxele_prediction','mesh','adcirc_mesh');
    ncwriteatt(f,'maxele_prediction','units','m');
    ncwriteatt(f,'maxele_prediction','location','node');
    ncwriteatt(f,'maxele_prediction','FillValue','-99999');

nccreate(f,'element','Dimensions',{'nele' size(fgs.e,1) 'nvertex' size(fgs.e,2)},'Format','netcdf4', 'Datatype', 'int32');
    ncwriteatt(f,'element','short_name','ele');
    ncwriteatt(f,'element','long_name','element');
    ncwriteatt(f,'element','standard_name','face_node_connectivity');
    ncwriteatt(f,'element','units','nondimensional');
    ncwriteatt(f,'element','start_index',1);

nccreate(f,'bnd','Dimensions',{'nbd' size(fgs.bnd,1) 'nbi' size(fgs.bnd,2)},'Format','netcdf4');
    ncwriteatt(f,'bnd','long_name','Boundary_Segment_Node_List');
    ncwriteatt(f,'bnd','standard_name','XXX');
    

% nccreate(f,'trigrid','Dimensions',{'nele' size(fgs.e,1) 'nvertex' size(fgs.e,2)},'Format','netcdf4');
%     ncwriteatt(f,'trigrid','domain_name', fgs.name);
%     ncwriteatt(f,'trigrid','grid_name','triangular_mesh');
%     ncwriteatt(f,'trigrid','Horizontal_Triangular_Element_Incidence_List','ele');
%     ncwriteatt(f,'trigrid','Boundary_Segment_Node_List','bnd');
% 	ncwriteatt(f,'trigrid','Index_start',1);
%     ncwriteatt(f,'trigrid','grid_type', 'Triangular');

    
ncwrite(f,'x', fgs.x);
ncwrite(f,'y', fgs.y);
ncwrite(f,'maxele', fgs.z);
ncwrite(f, 'maxele_prediction', fgs.zhat);
ncwrite(f, 'element', fgs.e);
ncdisp(f)