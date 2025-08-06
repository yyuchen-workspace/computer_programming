#ifndef MYLIBRARY_H_INCLUDED
#define MYLIBRARY_H_INCLUDED

#ifdef BUILD_DLL
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT __declspec(dllimport)
#endif

#ifdef __cplusplus
extern "C"
{
#endif


DLL_EXPORT void team();
DLL_EXPORT void sayhi();

#ifdef __cplusplus
}
#endif


#endif // MYLIBRARY_H_INCLUDED
