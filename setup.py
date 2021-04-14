from distutils.core import setup, Extension

pkg = 'Extensions.ChangeRootPassword'
setup(name='enigma2-plugin-extensions-changerootpassword',
       version='0.1',
       license='GPLv2',
       url='https://github.com/E2OpenPlugins',
       description='ChangeRootPassword',
       long_description='Set/Change your box password',
       author='meo',
       author_email='lupomeo@hotmail.com',
       packages=[pkg],
       package_dir={pkg: 'plugin'},
       package_data={pkg: ['*.png']}
      )
