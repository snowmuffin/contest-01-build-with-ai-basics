using System;
using System.IO;
using System.Text.Json;
using System.Windows;
using System.Windows.Media.Imaging;
using Aquarium.Core;

namespace Aquarium.Windows.Rendering;

// Asset placement only. Simulation geometry, depth bands and feeding stay in Core.
internal sealed class FishSpriteAtlas
{
    internal sealed record Sprite(BitmapSource Bitmap, int CanvasWidth, int CanvasHeight,
        double OffsetX, double OffsetY);
    private readonly Sprite[,,] frames = new Sprite[4,4,2];
    public Sprite this[FishSpecies species, FishFacing facing, int frame] => frames[(int)species,(int)facing,frame];

    public FishSpriteAtlas()
    {
        var atlas = new BitmapImage();
        atlas.BeginInit();atlas.CacheOption=BitmapCacheOption.OnLoad;
        atlas.UriSource=new Uri("pack://application:,,,/Aquarium.Windows;component/Assets/fish-sprites.png");
        atlas.EndInit();atlas.Freeze();
        var resource = Application.GetResourceStream(new Uri("pack://application:,,,/Aquarium.Windows;component/Assets/fish-sprites.json"))
            ?? throw new InvalidDataException("Fish sprite metadata is missing.");
        using var stream = resource.Stream;
        var metadata = JsonSerializer.Deserialize<AtlasInfo>(stream, new JsonSerializerOptions { PropertyNameCaseInsensitive=true })
            ?? throw new InvalidDataException("Fish sprite metadata is empty.");
        if(metadata.Version!=1 || metadata.Width!=atlas.PixelWidth || metadata.Height!=atlas.PixelHeight || metadata.Frames is null || metadata.Frames.Length!=32)
            throw new InvalidDataException("Fish sprite atlas/metadata layout is invalid.");
        foreach(var entry in metadata.Frames)
        {
            if(!Enum.TryParse<FishSpecies>(entry.Species, out var species) || !Enum.IsDefined(species) ||
               !Enum.TryParse<FishFacing>(entry.Facing, out var facing) || !Enum.IsDefined(facing) ||
               entry.Frame<0 || entry.Frame>1 || entry.X<0 || entry.Y<0 || entry.Width<=0 || entry.Height<=0 ||
               (long)entry.X+entry.Width>atlas.PixelWidth || (long)entry.Y+entry.Height>atlas.PixelHeight ||
               entry.CanvasWidth<entry.Width || entry.CanvasHeight<entry.Height ||
               !double.IsFinite(entry.OffsetX) || !double.IsFinite(entry.OffsetY) || entry.OffsetX<0 || entry.OffsetY<0 ||
               entry.OffsetX+entry.Width>entry.CanvasWidth || entry.OffsetY+entry.Height>entry.CanvasHeight ||
               frames[(int)species,(int)facing,entry.Frame] is not null)
                throw new InvalidDataException("Fish sprite frame mapping is invalid or duplicated.");
            var bitmap = new CroppedBitmap(atlas, new Int32Rect(entry.X,entry.Y,entry.Width,entry.Height));
            bitmap.Freeze();
            frames[(int)species,(int)facing,entry.Frame]=new Sprite(bitmap,entry.CanvasWidth,entry.CanvasHeight,entry.OffsetX,entry.OffsetY);
        }
    }

    private sealed record AtlasInfo(int Version, int Width, int Height, FrameInfo[] Frames);
    private sealed record FrameInfo(string Species, string Facing, int Frame, int X, int Y, int Width, int Height,
        int CanvasWidth, int CanvasHeight, double OffsetX, double OffsetY);
}
