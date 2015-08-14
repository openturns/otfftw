
#ifndef OTFFTW_PRIVATE_HXX
#define OTFFTW_PRIVATE_HXX

/* From http://gcc.gnu.org/wiki/Visibility */
/* Generic helper definitions for shared library support */
#if defined _WIN32 || defined __CYGWIN__
#define OTFFTW_HELPER_DLL_IMPORT __declspec(dllimport)
#define OTFFTW_HELPER_DLL_EXPORT __declspec(dllexport)
#define OTFFTW_HELPER_DLL_LOCAL
#else
#if __GNUC__ >= 4
#define OTFFTW_HELPER_DLL_IMPORT __attribute__ ((visibility ("default")))
#define OTFFTW_HELPER_DLL_EXPORT __attribute__ ((visibility ("default")))
#define OTFFTW_HELPER_DLL_LOCAL  __attribute__ ((visibility ("hidden")))
#else
#define OTFFTW_HELPER_DLL_IMPORT
#define OTFFTW_HELPER_DLL_EXPORT
#define OTFFTW_HELPER_DLL_LOCAL
#endif
#endif

/* Now we use the generic helper definitions above to define OTFFTW_API and OTFFTW_LOCAL.
 * OTFFTW_API is used for the public API symbols. It either DLL imports or DLL exports (or does nothing for static build)
 * OTFFTW_LOCAL is used for non-api symbols. */

#ifndef OTFFTW_STATIC /* defined if OT is compiled as a DLL */
#ifdef OTFFTW_DLL_EXPORTS /* defined if we are building the OT DLL (instead of using it) */
#define OTFFTW_API OTFFTW_HELPER_DLL_EXPORT
#else
#define OTFFTW_API OTFFTW_HELPER_DLL_IMPORT
#endif /* OTFFTW_DLL_EXPORTS */
#define OTFFTW_LOCAL OTFFTW_HELPER_DLL_LOCAL
#else /* OTFFTW_STATIC is defined: this means OT is a static lib. */
#define OTFFTW_API
#define OTFFTW_LOCAL
#endif /* !OTFFTW_STATIC */


#endif // OTFFTW_PRIVATE_HXX

