'''
Created on May 27, 2013

@author: tulvur
'''

import subprocess

class EulerReasoner(object):
    '''
    Gateway to call to euler/EYE resoner
    '''

    def __init__( self, euler_path='../../../../../' ):
        self.euler_path = euler_path + "" if euler_path.endswith("/") else "/"
    
    def _generic_query( self, input_files, query_file, optional_args, output_file_path = None ):
        '''
        This method invokes Euler (EYE) in the following way:
        
        java -jar path/Euler.jar [optional_args] [input_files] --query [goal_file] 
        '''
        
        call = ['java', '-jar', self.euler_path + 'Euler.jar']
        call += optional_args
        
        if isinstance(input_files, (list, tuple, set)):
            for input_file in input_files: # since "call += input_files" can only concatenate lists to lists
                call.append( input_file )
        else:
            call.append( input_files )
            
        call += ['--query', query_file]
        #print call
        output = subprocess.check_output( call )
        
        if output_file_path is None:
            return output
        else:
            with open (output_file_path, "w") as output_file:
                output_file.write( output )
                return output_file_path
            raise Exception("The plan could not be created.")
    
    def query( self, input_files, query_file, output_file_path = None  ):
        '''
        This method invokes Euler (EYE) in the following way:
        
        java -jar path/Euler.jar --nope [input_files] --query [goal_file] 
        '''
        return self._generic_query( input_files, query_file, ["--nope",], output_file_path )
    
    
    def query_proofs( self, input_files, query_file, output_file_path = None ):
        '''
        This method invokes Euler (EYE) in the following way:
        
        java -jar path/Euler.jar [input_files] --query [goal_file] 
        '''        
        return self._generic_query( input_files, query_file, [], output_file_path )        